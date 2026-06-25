# twse-data
Fetch twse data form

Old daily - "https://www.twse.com.tw/exchangeReport/STOCK_DAY_ALL?response=json"  
```ts
{  
  stat: string;
  date: string;  
  title: string;  
  fields: string[];  
  data: string[][];  
}
```
New daily "https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL"
```ts
[
  {  
    Date: string;  
    Code: string;  
    Name: string;  
    TradeVolume: string;  
    TradeValue: string;  
    Transaction: string;  
    OpeningPrice: string;  
    HighestPrice: string;  
    LowestPrice: string;  
    ClosingPrice: string;  
    Change: string;  
  },
]
```
