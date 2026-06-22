import requests, pandas as pd, json, os

url = "https://www.twse.com.tw/exchangeReport/TWTB4U?response=csv"
r = requests.get(url)
r.encoding = "utf-8"

os.makedirs("categories", exist_ok=True)

csv_path = "categories/fetch_twse_categories.csv"
with open(csv_path, "w", encoding="utf-8") as f:
    f.write(r.text)

df = pd.read_csv(csv_path)
df.columns = (
  df.columns
  .str.strip()
  .str.replace("\ufeff", "", regex=False)
)

stock_id_cols = ["證券代號", "股票代號", "代號"]
industry_cols = ["產業別", "產業分類", "產業"]
stock_col = next((c for c in stock_id_cols if c in df.columns), None)
industry_col = next((c for c in industry_cols if c in df.columns), None)

if stock_col is None or industry_col is None:
    raise ValueError(f"找不到必要欄位: {df.columns.tolist()}")
    
mapping = dict(zip(df[stock_col].astype(str).str.strip(), df[industry_col]).astype(str).strip())

json_path = "categories/fetch_twse_categories.json"
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(mapping, f, ensure_ascii=False, indent=2, sort_keys=True)
