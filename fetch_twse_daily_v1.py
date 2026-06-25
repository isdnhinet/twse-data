import requests, datetime, json, os, time

url = "https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL"

headers = { "User-Agent": "Mozilla/5.0" }

def normalize_date(raw_date: str) -> str:
    """
    if YYYMMDD to YYYYMMDD
    """
    if raw_date.isdigit():
        if len(raw_date) == 7:
            roc_year = int(raw_date[:3])
            ad_year = roc_year + 1911
            return f"{ad_year}{raw_date[3:]}"
        elif len(raw_date) == 8:
            return raw_date
    return datetime.date.today().strftime("%Y%m%d")

r = requests.get(url, headers=headers, timeout=30)
r.raise_for_status()
data = r.json()

if isinstance(data, list) and len(data) > 0:
    raw_date = (
        data[0].get("Date")
        or data[0].get("TradeDate")
        or datetime.date.today().strftime("%Y%m%d")
    )
    report_date = normalize_date(raw_date)
else:
    report_date = datetime.date.today().strftime("%Y%m%d")
    
os.makedirs("data/dayall", exist_ok=True)

path = f"data/dayall/{report_date}.json"

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"saved: data/dayall/{report_date}.json")
