# twse-data
fetch twse data form

old daily - "https://www.twse.com.tw/exchangeReport/STOCK_DAY_ALL?response=json"  
```ts
interface TwseStockDayAllOld {  
  stat: string;  
  date: string;  
  title: string;  
  fields: string[];  
  data: string[][];  
}
```
new daily "https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL"
```ts
interface TwseStockDayAllNew {  
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
}  
type TwseResponseNew = TwseStockDayAllNew[];
```
