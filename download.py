import os
import asyncio
from playwright.async_api import async_playwright

output_dir = "./pokemon_bmp"
os.makedirs(output_dir, exist_ok=True)

async def download_bmp_files():
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        # Navigate to the base tool
        await page.goto("https://basvanderploeg.nl/xteink/pokemon/", wait_until="networkidle")
        await page.wait_for_timeout(1000)

        START_ID = 152
        END_ID = 1025  # Adjust as needed (e.g., 1025 for all generations)

        for i in range(START_ID, END_ID + 1):
            try:
                # 1. Locate and fill the input/number field
                # Matches input fields or textboxes on the form
                input_field = page.locator("input[type='number'], input[type='text']").first
                await input_field.fill(str(i))
                
                # 2. Click the 'Update' button
                await page.click("text=Update")
                
                # Brief wait to let the page process and re-render the canvas
                await page.wait_for_timeout(400)

                # 3. Wait for download event and click 'Download .BMP'
                async with page.expect_download(timeout=10000) as download_info:
                    await page.click("text=Download .BMP")

                download = await download_info.value
                save_path = os.path.join(output_dir, f"{i:04d}.bmp")
                await download.save_as(save_path)
                print(f" Saved: Pokémon #{i:04d}")

            except Exception as e:
                print(f" Failed to download Pokémon #{i:04d}: {e}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(download_bmp_files())
