import os, json, re
import pandas as pd
from decimal import Decimal, InvalidOperation
from serpapi import GoogleSearch
import google.generativeai as genai




def to_money(x):
    if x is None:
        return None
    if isinstance(x, (int, float)):
        return float(x)
    s = str(x)
    s = re.sub(r"[^\d.]", "", s)
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def serpapi_shopping_search(query: str, location: str | None = None) -> list[dict]:
    api_key = os.getenv("serpapi_shopping_api")
    if not api_key:
        raise RuntimeError("Missing SERPAPI key: set env var serpapi_shopping_api")

    params = {
        "engine": "google_shopping",
        "q": query,
        "api_key": api_key,
        "gl": "my",
        "location": location or "Kuala Lumpur, Federal Territory of Kuala Lumpur, Malaysia",
    }

    results = GoogleSearch(params).get_dict()

    if "error" in results:
        raise RuntimeError(f"SerpApi error: {results['error']}")

    return results.get("shopping_results", [])




def results_to_df(shopping_results: list[dict], product_name: str, qty):
    df = pd.DataFrame(shopping_results)

    
    keep = ["title", "source", "price", "extracted_price", "rating", "reviews", "delivery", "product_link"]
    df = df.reindex(columns=[c for c in keep if c in df.columns])

    df["product"] = product_name
    df["quantity"] = qty

    
    if "extracted_price" in df.columns:
        df["unit_price"] = df["extracted_price"].apply(to_money)
    else:
        df["unit_price"] = df.get("price", None).apply(to_money)

    df["row_total"] = df["unit_price"] * df["quantity"].fillna(1)

    df = df[df["unit_price"].notna()].copy()

    return df

def build_master_df(result: dict) -> pd.DataFrame:
    all_dfs = []
    constraints = result.get("constraints", {})
    location = constraints.get("location")

    if not location or str(location).strip().lower() == "null":
        location = "Kuala Lumpur, Federal Territory of Kuala Lumpur, Malaysia"

    for item in result.get("items", []):
        name = item["name"]
        qty = item.get("quantity") or 1

        shopping_results = serpapi_shopping_search(name, location=location)
        df_item = results_to_df(shopping_results, product_name=name, qty=qty)
        all_dfs.append(df_item)

    return pd.concat(all_dfs, ignore_index=True) if all_dfs else pd.DataFrame()


def top_n_per_product(master: pd.DataFrame, n=10) -> pd.DataFrame:
    return (master
            .sort_values(["product", "unit_price"])
            .groupby("product", as_index=False)
            .head(n)
            .reset_index(drop=True))


def finalize_selection(selection_json: dict) -> tuple[pd.DataFrame, float]:
    selected = selection_json.get("selected", [])
    total = selection_json.get("total", 0)

    df_selected = pd.DataFrame(selected)
    return df_selected, float(total)







