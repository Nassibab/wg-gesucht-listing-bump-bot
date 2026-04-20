
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

from dotenv import load_dotenv
import os



load_dotenv()

username = os.getenv("WG_GESUCHT_USERNAME")
password = os.getenv("WG_GESUCHT_PASSWORD")



chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)


driver = webdriver.Chrome(options=chrome_options)


#driver.quit()
wait = WebDriverWait(driver, 15)
driver.get("https://www.wg-gesucht.de/meine-anzeigen.html")
accept = wait.until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="cmpwelcomebtnyes"]/a'))
)

driver.execute_script("arguments[0].click();", accept)

driver.find_element(
    By.XPATH,
    '//*[@id="main_column"]/div[1]/div/div/div/div/div[4]/div/div/a'
).click()



wait = WebDriverWait(driver, 10)

email_input = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="login_email_username"]')))
password_input = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="login_password"]')))

email_input.clear()
email_input.click()
email_input.send_keys(username)

password_input.clear()
password_input.click()
password_input.send_keys(password)

driver.find_element(By.XPATH, '//*[@id="login_submit"]').click()
# 1. Target the exact clickable span using its unique data-asset_id
dropdown_trigger = wait.until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, 'span.mdi-dots-vertical[data-asset_id="12041723"]')
))
dropdown_trigger.click()

# 2. Click the specific option (e.g., "Deaktivieren" / "Aktivieren")
# Using a text-based XPath or specific class makes this infinitely more stable
target_option = wait.until(EC.element_to_be_clickable(
    (By.XPATH, '//ul[contains(@class, "asset_actions_dropdown")]//a[contains(@class, "update_deactivated_status") and @data-asset_id="12041723"]')
))
target_option.click()

# 3. Confirm Modal
confirm_btn = wait.until(EC.element_to_be_clickable(
    (By.XPATH, '//*[@id="deactivated_modal"]//button')
))
confirm_btn.click()


# 1. Open the dropdown menu for the specific asset
dropdown_trigger = wait.until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, 'span.mdi-dots-vertical[data-asset_id="12041723"]')
))
dropdown_trigger.click()

# 2. Click the 'Aktivieren' option
# Notice we target data-deactivated="0" to ensure we hit the Activate button
activate_option = wait.until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, 'a.update_deactivated_status[data-asset_id="12041723"][data-deactivated="0"]')
))
activate_option.click()

# 3. Confirm the Modal
# The modal uses the same ID for both activating and deactivating
confirm_btn = wait.until(EC.element_to_be_clickable(
    (By.XPATH, '//*[@id="deactivated_modal"]//button')
))
confirm_btn.click()


