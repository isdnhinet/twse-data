import requests, datetime, json, os, time

url = "https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

r = requests.get(url, headers=headers, timeout=30)
r.raise_for_status()
data = r.json()

report_date = datetime.date.today().strftime("%Y%m%d")

os.makedirs("data/dayall", exist_ok=True)
with open(f"data/dayall/{report_date}.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"saved: data/dayall/{report_date}.json")
