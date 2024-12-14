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
    # chrome_options.add_argument("--headless")  # Uncomment for headless mode

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get("https://stellarium-web.org/")
    
    # Wait until the search box is present
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "input-33"))
    )
    
    # Search for the celestial body
    search_box.clear()
    search_box.send_keys(celestial_name)
    time.sleep(3)
    search_box.send_keys(Keys.TAB)
    search_box.send_keys(Keys.ENTER)
    search_box.send_keys(Keys.RETURN)
    
    
    
    ra_dec_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="stel"]/div/div/div[10]/div[3]/div[4]/div[2]'))
    )
    
    ra_dec_values = ra_dec_div.find_elements(By.XPATH, '/html/body/div[2]/div/div[1]/main/div/div/div/div/div/div[10]/div[3]/div[4]/div[2]')
    
    print(ra_dec_values)
    
    driver.quit()

get_celestial_coordinates("Mars")