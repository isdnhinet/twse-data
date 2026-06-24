import requests, datetime, json, os, time

url = "https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL"

headers = { "User-Agent": "Mozilla/5.0 }

r = requests.get(url, headers=headers, timeout=30)
r.raise_for_status()
data = r.json()

if isinstance(data, list) and len(data) > 0:
    report_date = (
        data[0].get("Date")
        or data[0].get("TradeDate")
        or datetime.date.today().strftime("%Y%m%d")
    )
else:
    report_date = datetime.date.today().strftime("%Y%m%d")
    
os.makedirs("data/dayall", exist_ok=True)

path = f"data/dayall/{report_date}.json"

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"saved: data/dayall/{report_date}.json")
