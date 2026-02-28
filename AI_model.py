import google.generativeai as genai
import os, json, re
import pandas as pd
from serpapi import GoogleSearch
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


def normalize_budget(b):
    if b is None:
        return None

    if isinstance(b, (int, float, Decimal)):
        d = Decimal(str(b))
        return str(d.quantize(Decimal("0.00"), rounding=ROUND_HALF_UP))

    s = str(b).strip()
    if not s:
        return None

    m = re.search(r"(\d+(?:,\d{3})*(?:\.\d+)?)", s)
    if not m:
        return None

    num = m.group(1).replace(",", "")
    try:
        d = Decimal(num)
        return str(d.quantize(Decimal("0.00"), rounding=ROUND_HALF_UP))
    except InvalidOperation:
        return None



class AiModelGemini:
    def __init__(self, model_name: str =  "models/gemini-2.5-flash"):
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("Missing GEMINI_API_KEY environment variable.")
        genai.configure(api_key=api_key)

        # Keep schema as an attribute so other methods can use it 
        # schema obtained using AI 
        self.schema = {
            "type": "object",
            "properties": {
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string"
                            },
                            "quantity": {
                                "type": "integer"
                            },
                            "notes": {
                                "type": "string"
                            }
                        },
                        "required": ["name"]   # quantity & notes optional
                    }
                },
                "constraints": {
                    "type": "object",
                    "properties": {
                        "budget": {
                            "type": "string"   # must be formatted like "50.00"
                        },
                        "currency": {
                            "type": "string"
                        },
                        "location": {
                            "type": "string"
                        }
                    }
                    # none required (all optional)
                },
                "raw": {
                    "type": "string"
                }
            },
            "required": ["items", "constraints", "raw"]
        }


        self.model = genai.GenerativeModel(model_name)

       
        self.prompt_template = """You are a strict structured data extraction engine.

Return ONLY valid JSON. No explanations. No markdown. No extra text.

Schema (must match exactly):
{{
  "items": [{{"name": "string", "quantity": "integer|null", "notes": "string|null"}}],
  "constraints": {{"budget": "string|null", "currency": "string|null", "location": "string|null"}},
  "raw": "string"
}}

Rules:
- Extract only products the user wants to buy.
- "name" should be short and generic.
- quantity only if explicitly stated, else null.
- Put item-specific details in notes, else null.
- budget/currency/location only if explicitly stated, else null.
- "raw" must copy the user request exactly.

User request:
"{user_input}"
"""
    

    def extract(self, user_input: str) -> dict:
        prompt= self.prompt_template.format(user_input=user_input)


        response = self.model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.0,
                "response_mime_type": "application/json",
                "response_schema": self.schema,
    },
)

        
        try:
            parsed = json.loads(response.text)
            return self._normalize(parsed)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Model returned invalid JSON: {response.text}") from e
    
    def _normalize(self, data: dict) -> dict:
        data.setdefault("items", [])
        data.setdefault("constraints", {})
        data.setdefault("raw", "")

        c = data["constraints"]
        c.setdefault("budget", None)
        cur = c.get("currency")
        if cur is None or str(cur).strip().lower() in {"", "null", "none"}:
            c["currency"] = None

        loc = c.get("location")
        if loc is None or str(loc).strip().lower() in {"", "null", "none"}:
            c["location"] = "Malaysia"

        c["budget"] = normalize_budget(c.get("budget"))

        for it in data["items"]:
            it.setdefault("quantity", 1)
            it.setdefault("notes", None)

        return data



def gemini_choose_best(candidates_df: pd.DataFrame, constraints: dict) -> dict:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel("models/gemini-2.5-flash")  # fast + cheap-ish

    budget = constraints.get("budget")
    currency = constraints.get("currency")
    location = constraints.get("location")

    # shrink payload from AI 
    payload = candidates_df[["product","title","source","unit_price","quantity","row_total","product_link","rating","reviews"]].to_dict(orient="records")

    prompt = f"""
        You are selecting shopping options.
        Goal: choose ONE best option per product, respecting overall budget if provided.

        Constraints:
        - budget: {budget}
        - currency: {currency}
        - location: {location}

        Rules:
        - Prefer lowest total cost, but consider quality signals (rating/reviews) when price is close.
        - If budget is not enough for all items, choose a subset that maximizes value (cover as many items as possible).
        - Return STRICT JSON only with this schema:

        {{
        "selected": [
            {{
            "product": string,
            "title": string,
            "unit_price": number,
            "quantity": number,
            "row_total": number,
            "product_link": string
            }}
        ],
        "total": number
        }}

        Candidates:
        {json.dumps(payload)[:200000]}
        """

    resp = model.generate_content(
        prompt,
        generation_config={"response_mime_type": "application/json", "temperature": 0.0},
        )
    return json.loads(resp.text)


