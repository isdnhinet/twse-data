from pathlib import Path
import json

FIELD_MAP = {
    "證券代號": "Code",
    "證券名稱": "Name",
    "成交股數": "TradeVolume",
    "成交金額": "TradeValue",
    "開盤價": "OpeningPrice",
    "最高價": "HighestPrice",
    "最低價": "LowestPrice",
    "收盤價": "ClosingPrice",
    "漲跌價差": "Change",
    "成交筆數": "Transaction",
}

def convert_date_to_roc(d):
    date_str = d.replace("-", "").replace("/", "")
    year = int(date_str[:4]) - 1911
    rest = date_str[4:]

    return f"{year}{rest}"

def clean_value(field, value):
    if isinstance(value, str):
        return value.replace(",", "").replace("+", "")
    if field == "Change" and value not in (None, ""):
        try: 
            return f"{float(value):.4f}"
        except: 
            return value
    return value

def convert_old_to_new(old):
    date = convert_date_to_roc(old["date"])
    new_data = []

    for row in old["data"]:
        item = { "Date": date }

        for field, value in zip(old["fields"], row):
            if field in FIELD_MAP:
                item[FIELD_MAP[field]] = clean_value(field, value)
        
        new_data.append(item)
    return new_data

output_dir = Path("dayall")
output_dir.mkdir(exist_ok=True)

for file in Path("data").glob("*.json"):
    with open(file, encoding="utf-8") as f:
        data = json.load(f)

    #if isinstance(data, list):
     #   print("Already new format")
      #  continue

    new_data = convert_old_to_new(data)

    output_path = output_dir / file.name

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)

    print("converted -> {output_path}")
