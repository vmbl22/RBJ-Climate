from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import os, time

# === SETUP ===
raw_folder = "forecast_screenshots"
cropped_folder = "forecast_screenshots_cropped"
os.makedirs(raw_folder, exist_ok=True)
os.makedirs(cropped_folder, exist_ok=True)

# Crop box for Southern Africa (left, top, right, bottom)
# Adjust if needed
crop_box = (300, 300, 900, 730)

# === SELENIUM CONFIG ===
options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1400,1000")  # Ensure no scrollbars or UI overlaps
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Load the forecast page
driver.get("https://www.cpc.ncep.noaa.gov/products/international/cpci/data/00/gfs_precip_24h_africa.html")
print("⏳ Waiting for page to fully load...")
time.sleep(4)  # Extended wait to ensure map loads and scrolls into place (especially Day 1)

# === LOOP THROUGH FORECAST DAYS ===
for day in range(1, 7):
    if day > 1:
        time.sleep(2)  # Short wait for each step to render new map

    # Save full screenshot
    full_path = os.path.join(raw_folder, f"day{day}.png")
    driver.save_screenshot(full_path)
    print(f"📸 Saved full screenshot: {full_path}")

    # Crop to SADC extent
    img = Image.open(full_path)
    cropped = img.crop(crop_box)

    cropped_path = os.path.join(cropped_folder, f"day{day}_sadc.png")
    cropped.save(cropped_path)
    print(f"✂️ Cropped to SADC region: {cropped_path}")

    # Click "Step >" to move to next day
    try:
        step_button = driver.find_element(By.XPATH, "//input[@value='Step >']")
        step_button.click()
    except Exception as e:
        print(f"⚠️ Could not click 'Step >': {e}")
        break

driver.quit()
print("\n✅ Done! All SADC maps (Day 1–6) saved and cropped successfully.")
