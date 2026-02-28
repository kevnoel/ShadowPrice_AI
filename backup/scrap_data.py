from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import json
import sys
sys.set_int_max_str_digits(0)  # unlimited
import AI_model
import functions

app = FastAPI()

# Serve your index.html folder (same folder as scrap_data.py)
app.mount("/static", StaticFiles(directory="."), name="static")


@app.get("/", response_class=HTMLResponse)
def home():
    # If your file is literally "index.html" in the same folder:
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.post("/run", response_class=HTMLResponse)
def run_pipeline(user_text: str = Form(...)):
    ai = AI_model.AiModelGemini()
    extracted = ai.extract(user_text)

    master = functions.build_master_df(extracted)
    candidates = functions.top_n_per_product(master, n=10)
    decision = AI_model.gemini_choose_best(candidates, extracted["constraints"])
    df_selected, total = functions.finalize_selection(decision)

    # Convert df to list of dicts for easy HTML building
    rows = df_selected.to_dict(orient="records")

    budget = extracted["constraints"].get("budget")
    currency = extracted["constraints"].get("currency") or ""
    location = extracted["constraints"].get("location") or "Kuala Lumpur, Federal Territory of Kuala Lumpur, Malaysia"

    # Build a simple nice HTML
    # Build a simple nice HTML
    html = f"""
            <html>
            <head>
            <meta charset="utf-8" />
            <title>Results</title>
            <style>
                body {{
                font-family: ui-sans-serif, system-ui, Arial;
                padding: 24px;
                background: #0b1220;
                color: #e8eefc;
                }}

                h2 {{
                margin-bottom: 18px;
                }}

                .meta {{
                margin-bottom: 20px;
                }}

                .pill {{
                display:inline-block;
                padding:6px 14px;
                border-radius:999px;
                background: linear-gradient(135deg, #6aa9ff, #8b5cf6);
                color: #081022;
                font-weight: 700;
                margin-right:8px;
                }}

                table {{
                border-collapse: collapse;
                width: 100%;
                border-radius: 14px;
                overflow: hidden;
                background: rgba(255,255,255,0.05);
                border: 1px solid rgba(255,255,255,0.14);
                }}

                th, td {{
                padding: 12px;
                text-align: left;
                }}

                th {{
                background: rgba(255,255,255,0.08);
                color: rgba(232,238,252,0.85);
                font-size: 12px;
                text-transform: uppercase;
                letter-spacing: 0.6px;
                }}

                td {{
                border-top: 1px solid rgba(255,255,255,0.08);
                color: rgba(232,238,252,0.92);
                font-size: 14px;
                }}

                tr:nth-child(even) {{
                background: rgba(255,255,255,0.04);
                }}

                tr:hover {{
                background: rgba(106,169,255,0.10);
                }}

                a {{
                color: #6aa9ff;
                font-weight: 700;
                text-decoration: none;
                }}

                a:hover {{
                text-decoration: underline;
                }}
            </style>
            </head>
            <body>

            <h2>Selected items</h2>

            <div class="meta">
                <span class="pill">Location: {location}</span>
                <span class="pill">Budget: {budget or "Not provided"} {currency}</span>
                <span class="pill">Total: {total:.2f} {currency}</span>
            </div>

            <table>
                <thead>
                <tr>
                    <th>Product</th>
                    <th>Option</th>
                    <th>Unit price</th>
                    <th>Qty</th>
                    <th>Row total</th>
                    <th>Link</th>
                </tr>
                </thead>
                <tbody>
            """


    for r in rows:
        link = r.get("product_link", "")
        html += f"""
          <tr>
            <td>{r.get("product","")}</td>
            <td>{r.get("title","")}</td>
            <td>{r.get("unit_price","")}</td>
            <td>{r.get("quantity","")}</td>
            <td>{r.get("row_total","")}</td>
            <td><a href="{link}" target="_blank" rel="noopener">Open</a></td>
          </tr>
        """

    html += """
        </tbody>
      </table>

      <br/>
      <a href="/">← Back</a>
    </body>
    </html>
    """
    return html
