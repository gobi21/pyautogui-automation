import asyncio
import csv
from playwright.async_api import async_playwright

# Official NSE API endpoint for Nifty 50
NIFTY_API = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050"


async def download_nifty50_csv():

    async with async_playwright() as p:

        # Launch browser (used for session + fingerprint)
        browser = await p.chromium.launch(headless=True)

        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/121.0.0.0 Safari/537.36"
            ),
            locale="en-US"
        )

        request = context.request

        # Step 1: Warm-up request to generate cookies
        await request.get(
            "https://www.nseindia.com",
            headers={
                "accept": "text/html",
                "accept-language": "en-US,en;q=0.9"
            }
        )

        # Step 2: Call Nifty 50 API
        response = await request.get(
            NIFTY_API,
            headers={
                "accept": "application/json",
                "referer": "https://www.nseindia.com/",
                "x-requested-with": "XMLHttpRequest"
            }
        )

        if response.status != 200:
            print(f"❌ Failed to fetch data. Status: {response.status}")
            await browser.close()
            return

        json_data = await response.json()

        stocks = json_data.get("data", [])

        if not stocks:
            print("❌ No stock data received.")
            await browser.close()
            return

        # Step 3: Dynamically collect all keys (API may vary)
        all_keys = set()
        for stock in stocks:
            all_keys.update(stock.keys())

        all_keys = list(all_keys)

        # Step 4: Save to CSV
        with open("nifty50_list.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=all_keys,
                extrasaction="ignore"
            )
            writer.writeheader()
            writer.writerows(stocks)

        print("✅ Nifty 50 CSV downloaded successfully!")
        print("📁 File saved as: nifty50_list.csv")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(download_nifty50_csv())