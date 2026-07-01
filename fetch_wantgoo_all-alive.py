import asyncio
import json
from playwright.async_api import async_playwright

async def fetch_wantgoo():
  async with async_playwright() as p:
  
    # 啟動瀏覽器
    browser = await p.chromium.launch(headless=True)
    page = await browser.new_page()

    # 開網頁，通過 Cloudflare 驗證並取得 Cookie
    await page.goto("https://www.wantgoo.com/investrue")
    # 等待頁面載入與驗證
    await page.wait_for_timeout(5000)

    # 在瀏覽器環境呼叫 API
    data = await page.evaluate("""
        async () => {
            const res = await fetch("https://www.wantgoo.com/investrue/all-alive", {
                method: "GET",
                headers: {
                    "Referer": "https://www.wantgoo.com/investrue"
                }
            });
            return await res.json();
        }
    """)

    await browser.close()
    return data
