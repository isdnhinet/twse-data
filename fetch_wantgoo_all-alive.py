import asyncio, json, os
from playwright.async_api import async_playwright

async def fetch_wantgoo():
  async with async_playwright() as p:
  
    # 啟動瀏覽器
    browser = await p.chromium.launch(headless=True)
    page = await browser.new_page()


    # 1. 先進入主頁，讓 Cloudflare 驗證
    await page.goto("https://www.wantgoo.com/index/listed/industry")
    await page.wait_for_timeout(5000)  # 等待驗證完成

    # 2. 取得 cookie
    cookies = await page.context.cookies()
    cookie_header = "; ".join([f"{c['name']}={c['value']}" for c in cookies])

    # 3. 用帶 cookie 的 request 打 API
    response = await page.request.get(
        "https://www.wantgoo.com/investrue/all-alive",
        headers={
            "Referer": "https://www.wantgoo.com/index/listed/industry",
            "Cookie": cookie_header
        }
    )
    
    # 4. 解析 JSON
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
