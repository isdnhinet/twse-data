import asyncio, json, os
from playwright.async_api import async_playwright

URL_PAGE = "https://www.wantgoo.com/index/listed/industry"
URL_API = "https://www.wantgoo.com/investrue/all-alive"

async def run():
    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
            ],
        )

        # ✅ 關鍵：持久 context（讓 CF 認為是同一人）
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
            viewport={"width": 1280, "height": 720},
        )

        page = await context.new_page()

        print("===== WARM UP PAGE =====")

        await page.goto(URL_PAGE, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)

        # 模擬人類行為
        await page.mouse.move(200, 300)
        await page.wait_for_timeout(1000)
        await page.mouse.move(400, 500)
        await page.wait_for_timeout(1500)

        print("===== GET COOKIES =====")

        cookies = await context.cookies()
        cookie_header = "; ".join([f"{c['name']}={c['value']}" for c in cookies])

        print("===== CALL API =====")

        # retry 機制（很重要）
        for i in range(3):
            try:
                resp = await page.request.get(
                    URL_API,
                    headers={
                        "Referer": URL_PAGE,
                        "Cookie": cookie_header,
                        "X-Requested-With": "XMLHttpRequest"
                    }
                )

                print("STATUS:", resp.status)

                if resp.status == 200:
                    data = await resp.json()
                    return data

            except Exception as e:
                print("retry error:", e)

            await page.wait_for_timeout(2000 * (i + 1))

        raise Exception("failed after retries")

async def main():
    data = await run()

    os.makedirs("data/wantgoo", exist_ok=True)

    with open("data/wantgoo/wantgoo.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("saved")

if __name__ == "__main__":
    asyncio.run(main())
