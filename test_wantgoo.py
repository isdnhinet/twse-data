import asyncio
import json
import os
from playwright.async_api import async_playwright, TimeoutError

URL = "https://www.wantgoo.com/index/listed/industry"


async def main():
    os.makedirs("data/wantgoo", exist_ok=True)

    result = {
        "goto_status": None,
        "url": None,
        "title": None,
        "cookies": [],
        "has_cf_clearance": False,
        "html_head": "",
    }

    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=True,
        )

        page = await browser.new_page()

        # ===== Network Log =====

        page.on(
            "response",
            lambda r: print(f"<< {r.status} {r.url}")
        )

        page.on(
            "requestfailed",
            lambda r: print(f"FAILED {r.url} {r.failure}")
        )

        page.on(
            "console",
            lambda msg: print(f"CONSOLE {msg.type}: {msg.text}")
        )

        print("===== START =====")

        try:
            response = await page.goto(
                URL,
                wait_until="load",
                timeout=30000,
            )

            if response:
                result["goto_status"] = response.status
                print("Goto Status:", response.status)

        except TimeoutError:
            print("Goto Timeout")

        except Exception as e:
            print("Goto Exception:", e)

        # 多等幾秒讓 JS / Cloudflare 跑
        await page.wait_for_timeout(5000)

        # 基本資訊
        result["url"] = page.url
        print("Current URL:", page.url)

        try:
            result["title"] = await page.title()
            print("Title:", result["title"])
        except Exception as e:
            print("Title Error:", e)

        # Cookies
        cookies = await page.context.cookies()

        result["cookies"] = cookies
        result["has_cf_clearance"] = any(
            c["name"] == "cf_clearance"
            for c in cookies
        )

        print("Cookie Count:", len(cookies))
        print("Has cf_clearance:", result["has_cf_clearance"])

        for c in cookies:
            print(c["name"], "=", c["value"][:40])

        # HTML
        html = await page.content()

        result["html_head"] = html[:2000]

        print("\n===== HTML HEAD =====")
        print(html[:2000])

        # Screenshot（如果需要可下載 artifact 查看）
        await page.screenshot(
            path="data/wantgoo/debug.png",
            full_page=True,
        )

        with open(
            "data/wantgoo/debug.html",
            "w",
            encoding="utf-8",
        ) as f:
            f.write(html)

        with open(
            "data/wantgoo/debug.json",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(
                result,
                f,
                ensure_ascii=False,
                indent=2,
            )

        await browser.close()

    print("===== END =====")


if __name__ == "__main__":
    asyncio.run(main())
