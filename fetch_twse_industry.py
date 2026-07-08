import pandas as pd, requests, certifi, os
from io import StringIO
from pathlib import Path

url = "https://isin.twse.com.tw/isin/C_public.jsp?strMode=2"

response = requests.get(
    url,
    verify=certifi.where()
)

response.encoding = "big5"

df = pd.read_html(
    StringIO(response.text),
    header=0
)[0]

result = []

kind = None

for _, row in df.iterrows():

    # 分類列，例如 股票、ETF、上市認購(售)權證
    if row.nunique(dropna=True) == 1:
        kind = row.iloc[0]
        continue

    code_name = str(row["有價證券代號及名稱"]).split()

    if len(code_name) >= 2:
        code = code_name[0]
        name = "".join(code_name[1:])
    else:
        code = row["有價證券代號及名稱"]
        name = None

    date = row["上市日"]

    if pd.notna(date):
        date = str(date).replace("/", "")

    result.append({
        "Code": code,
        "Name": name,
        "ISIN": row["國際證券辨識號碼(ISIN Code)"],
        "ListedDate": date,
        "Market": row["市場別"],
        "Industry": row["產業別"],
        "CFICode": row["CFICode"],
        "SecurityType": kind
    })

output_dir = Path("industry/twse")
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "stock-industry-twse.json"

pd.DataFrame(result).to_json(
    output_file,
    orient="records",
    force_ascii=False,
    indent=2
)

print(f"Saved: {output_file}")
