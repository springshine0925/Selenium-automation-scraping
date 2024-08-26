import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from output import Output

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration
CHROMEDRIVER_PATH = 'chromedriver.exe'
URL = "https://www.sharbatly.club/collections/all"
OUTPUT_FILE = "sharbatly.txt"
ELEMENT_CLASS = "footer"
PRODUCT_LIST_CLASS = "product-list"
LANG_PREFERENCE = 'en'
i = 0

# Setup WebDriver options
def setup_driver():
    options = Options()
    options.add_experimental_option("detach", False)
    options.add_argument(f"--lang={LANG_PREFERENCE}")
    prefs = {"translate_whitelists": {"ar": "en"}, "translate": {"enabled": "true"}}
    options.add_experimental_option("prefs", prefs)
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Main script
def main():
    try:
        driver = setup_driver()
        driver.get(URL)
        
        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located((By.ID, "locksmith-content")))

        label_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='city-2']")))
        label_element.click()
        time.sleep(2)

        scroll_until_element_found(driver, ELEMENT_CLASS, wait)

        time.sleep(1)
        elements_in_product_list = get_elements_by_class(driver, PRODUCT_LIST_CLASS, wait)

        save_elements_to_file(elements_in_product_list, OUTPUT_FILE)

    except Exception as e:
        logging.error("An error occurred: %s", str(e))
    finally:
        time.sleep(1)
        Output()
        time.sleep(3)
        driver.quit()

# Function to scroll and check for an element
def scroll_until_element_found(driver, target_class, wait, max_duration=200):
    start_time = time.time()
    while True:
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, PRODUCT_LIST_CLASS)))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            wait.until(EC.visibility_of_element_located((By.CLASS_NAME, target_class)))
            i = i + 1
            logging.info("Element with class '%s' found. Scrolling stopped.", target_class)
            if i > 50:
                logging.info("Break the loop...")
                break
        except:
            if time.time() - start_time >= max_duration:
                logging.warning("Time has elapsed without finding the element.")
                break

# Function to get elements by class name
def get_elements_by_class(driver, class_name, wait):
    element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, class_name)))
    return element.find_elements(By.XPATH, ".//*")

# Function to save elements to a file
def save_elements_to_file(elements, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        for element in elements:
            file.write(element.get_attribute("outerHTML") + "\n")
    logging.info("Elements saved to %s", file_path)

if __name__ == "__main__":
    main()
