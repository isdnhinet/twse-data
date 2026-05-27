import requests, datetime, json, os

url = "https://www.twse.com.tw/exchangeReport/STOCK_DAY_ALL?response=json"
r = requests.get(url)
data = r.json()

today = datetime.date.today().strftime("%Y%m%d")
os.makedirs("data", exist_ok=True)
with open(f"data/{today}.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
