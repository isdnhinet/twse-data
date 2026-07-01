import asyncio, json, os
from playwright.async_api import async_playwright

async def fetch_wantgoo():
  async with async_playwright() as p:
  
    # 啟動瀏覽器
    browser = await p.chromium.launch(headless=True)
    page = await browser.new_page()

    await page.goto("https://www.wantgoo.com/investrue") # 開網頁，通過 Cloudflare 驗證並取得 Cookie
    await page.wait_for_timeout(5000) # 等待頁面載入與驗證

    # 用 page.request.get 取得 API JSON
    response = await page.request.get(
      "https://www.wantgoo.com/investrue/all-alive",
      headers={"Referer": "https://www.wantgoo.com/investrue"}
    )
    data = await response.json()

    await browser.close()
    return data
    
if __name__ == "__main__":
  result = asyncio.run(fetch_wantgoo())
  
  # 存成檔案
  os.makedirs("data/wantgoo", exist_ok=True)
  path = "data/wantgoo/wantgoo.json"
  
  with open(path, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

  print(f"saved: {path}")
