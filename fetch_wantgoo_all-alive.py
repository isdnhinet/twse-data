import asyncio, json, os
from playwright.async_api import async_playwright

async def fetch_wantgoo():
  async with async_playwright() as p:
    browser = await p.chromium.launch(headless=True)
    page = await browser.new_page()

    # 1. 先進入主頁，讓 Cloudflare 驗證
    await page.goto(
      "https://www.wantgoo.com/index/listed/industry",
      wait_until="networkidle",
      timeout=60000
    )

    # ===== 診斷 Cloudflare 狀態 =====
    print("Current URL:", page.url)
    print("Page title:", await page.title())
    html = await page.content()
    if any(x in html.lower() for x in [
            "checking your browser",
            "just a moment",
            "cf-browser-verification",
            "challenge-platform",
            "turnstile",
        ]):
            print("⚠️ Cloudflare Challenge detected!")

    # 2. 取得 cookie
    cookies = await page.context.cookies()
    print("Cookies:", cookies)

    # ===== 診斷 Cookie 狀態 =====
    cf_cookie = next(
      (c for c in cookies if c["name"] == "cf_clearance"),
      None
    )
    if cf_cookie:
        print("✅ cf_clearance =", cf_cookie["value"][:20] + "...")
    else:
        print("❌ No cf_clearance cookie")

    print("User-Agent:", await page.evaluate("navigator.userAgent"))
    
    # 截圖方便 GitHub Actions Debug
    await page.screenshot(path="debug.png", full_page=True)
    
    # HTML 存起來
    with open("debug.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    # ====================================

    cookie_header = "; ".join([f"{c['name']}={c['value']}" for c in cookies])

    # 3. 用帶 cookie 的 request 打 API
    response = await page.request.get(
        "https://www.wantgoo.com/investrue/all-alive",
        headers={
            "Referer": "https://www.wantgoo.com/index/listed/industry",
            "Cookie": cookie_header
        }
    )
    
    print("API status:", response.status)
    
    # 4. 解析 JSON
    content = await response.text()
    print("DEBUG:", content[:200])

    if response.status !=200:
      raise Exception(f"API failed: {response.status}")
    
    data = await response.json()

    await browser.close()
    return data

if __name__ == "__main__":
  result = asyncio.run(fetch_wantgoo())

  os.makedirs("data/wantgoo", exist_ok=True)
  
  with open("data/wantgoo/wantgoo.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
