import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

username = os.getenv("WG_GESUCHT_USERNAME")
password = os.getenv("WG_GESUCHT_PASSWORD")

if not username or not password:
    raise ValueError("WG_GESUCHT_USERNAME and WG_GESUCHT_PASSWORD must be set as environment variables")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
# NOTE: "detach" experimental option removed — it crashes on Linux CI

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 15)

try:
    # ── Step 1: Load page and accept cookie banner ────────────────────────────
    print("Loading wg-gesucht...")
    driver.get("https://www.wg-gesucht.de/meine-anzeigen.html")

    try:
        accept = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="cmpwelcomebtnyes"]/a'))
        )
        driver.execute_script("arguments[0].click();", accept)
        print("Cookie banner accepted")
    except Exception:
        print("Cookie banner not found or already dismissed — continuing")

    # ── Step 2: Click the login button ───────────────────────────────────────
    print("Clicking login button...")
    driver.find_element(
        By.XPATH,
        '//*[@id="main_column"]/div[1]/div/div/div/div/div[4]/div/div/a'
    ).click()

    # ── Step 3: Fill in credentials ──────────────────────────────────────────
    print("Entering credentials...")
    email_input = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="login_email_username"]')))
    password_input = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="login_password"]')))

    email_input.clear()
    email_input.send_keys(username)
    password_input.clear()
    password_input.send_keys(password)

    driver.find_element(By.XPATH, '//*[@id="login_submit"]').click()
    print("Login submitted")

    # Wait for page to settle after login
    time.sleep(3)

    # ── Step 4: Deactivate listing ────────────────────────────────────────────
    print("Opening dropdown to deactivate listing...")
    dropdown_trigger = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'span.mdi-dots-vertical[data-asset_id="12041723"]')
    ))
    driver.execute_script("arguments[0].click();", dropdown_trigger)

    print("Clicking deactivate option...")
    target_option = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//ul[contains(@class, "asset_actions_dropdown")]//a[contains(@class, "update_deactivated_status") and @data-asset_id="12041723"]')
    ))
    driver.execute_script("arguments[0].click();", target_option)

    print("Confirming deactivation modal...")
    confirm_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="deactivated_modal"]//button')
    ))
    driver.execute_script("arguments[0].click();", confirm_btn)
    print("Listing deactivated")

    time.sleep(2)

    # ── Step 5: Re-activate listing ───────────────────────────────────────────
    print("Opening dropdown to reactivate listing...")
    dropdown_trigger = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'span.mdi-dots-vertical[data-asset_id="12041723"]')
    ))
    driver.execute_script("arguments[0].click();", dropdown_trigger)

    print("Clicking activate option...")
    activate_option = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'a.update_deactivated_status[data-asset_id="12041723"][data-deactivated="0"]')
    ))
    driver.execute_script("arguments[0].click();", activate_option)

    print("Confirming reactivation modal...")
    confirm_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="deactivated_modal"]//button')
    ))
    driver.execute_script("arguments[0].click();", confirm_btn)
    print("Listing reactivated successfully")

except Exception as e:
    print(f"ERROR: {e}")
    # Save a screenshot so you can see exactly what the browser sees on failure
    driver.save_screenshot("error_screenshot.png")
    print("Screenshot saved to error_screenshot.png")
    raise

finally:
    driver.quit()
    print("Browser closed")
