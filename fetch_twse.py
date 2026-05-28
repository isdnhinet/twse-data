import requests, datetime, json, os

url = "https://www.twse.com.tw/exchangeReport/STOCK_DAY_ALL?response=json"
r = requests.get(url)
data = r.json()

# 嘗試從 API 回傳的 JSON 裡抓日期欄位
report_date = data.get("date") or data.get("reportDate")

# 如果 API 沒有提供日期，就退回用今天日期
if not report_date:
    from datetime import date
    report_date = date.today().strftime("%Y%m%d")
    
os.makedirs("data", exist_ok=True)
with open(f"data/{report_date}.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
