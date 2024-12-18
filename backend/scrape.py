from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_celestial_coordinates(celestial_name):
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Run in headless mode for faster execution
    # chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("https://stellarium-web.org/")

        # Wait for the search input to be visible
        search_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"]'))
        )

        # Enter the celestial name in the search box
        search_box.clear()
        search_box.send_keys(celestial_name)
        time.sleep(3)  # Allow suggestions to load
        search_box.send_keys(Keys.ENTER)

        # Wait for the coordinates section to load
        coords_div = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "info-item"))
        )

        # Extract RA/Dec and Az/Alt values
        ra_dec = driver.find_element(By.XPATH, "//div[contains(text(), 'RA/Dec')]/following-sibling::div").text
        az_alt = driver.find_element(By.XPATH, "//div[contains(text(), 'Az/Alt')]/following-sibling::div").text

        print(f"RA/Dec: {ra_dec}")
        print(f"Az/Alt: {az_alt}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

# Example usage
get_celestial_coordinates("Mars")
