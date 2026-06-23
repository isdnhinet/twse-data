import requests, datetime, json, os, time

URL = "https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL"
r = requests.get(url, timeout=30)
r.raise_for_status()
data = r.json()

report_date = date.today().strftime("%Y%m%d")

os.makedirs("data", exist_ok=True)
with open(f"data/{report_date}.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"saved: data/{report_date}.json")
