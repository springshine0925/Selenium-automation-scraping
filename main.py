import os
import time
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load configuration from a separate file
CONFIG = {
    "url": "https://www.sharbatly.club/collections/all",
    "wait_time": 10,
    "max_scroll_duration": 300,  # 5 minutes
    "target_class": "footer",
    "output_file": "sharbatly.txt"
}

# Set up logging
logging.basicConfig(
    filename=f"sharbatly_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def scroll_to_target_element(driver, wait, target_class, max_duration):
    start_time = time.time()

    while True:
        # Scroll down the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Check if the target element is visible
        try:
            element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, target_class)))
            logging.info(f"Element with class {target_class} found. Scrolling stopped.")
            return element
        except:
            pass

        # Check if the maximum duration has been reached
        elapsed_time = time.time() - start_time
        if elapsed_time >= max_duration:
            logging.info(f"{max_duration} seconds have elapsed. Breaking the loop.")
            return None

def scrape_sharbatly_data():
    with webdriver.Chrome() as driver:
        driver.get(CONFIG["url"])
        wait = WebDriverWait(driver, CONFIG["wait_time"])

        try:
            form = wait.until(EC.visibility_of_element_located((By.ID, "locksmith-content")))
            label_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='city-2']")))
            label_element.click()
            time.sleep(2)

            element = scroll_to_target_element(driver, wait, CONFIG["target_class"], CONFIG["max_scroll_duration"])
            if element:
                product_list_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "product-list")))
                elements_in_product_list = product_list_element.find_elements_by_xpath(".//*")

                with open(CONFIG["output_file"], "w", encoding="utf-8") as file:
                    for element in elements_in_product_list:
                        file.write(element.get_attribute("outerHTML") + "\n")

                logging.info(f"Data saved to {CONFIG['output_file']}")
            else:
                logging.error("Failed to find the target element.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")

        time.sleep(2)
        logging.info("Closing the browser session.")

if __name__ == "__main__":
    scrape_sharbatly_data()
