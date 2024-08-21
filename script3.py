from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
from output3 import Output3

def setup_driver():
    options = Options()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")
    options.add_experimental_option("detach", True)
    options.add_argument("--lang=en")
    prefs = {
        "translate_whitelists": {"ar": "en"},
        "translate": {"enabled": "true"}
    }
    options.add_experimental_option("prefs", prefs)
    service = Service(executable_path='./chromedriver.exe')
    return webdriver.Chrome(service=service, options=options)


def accept_cookies(driver):
    wait = WebDriverWait(driver, 10)
    try:
        # accept_button = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
        accept_button =  wait.until(EC.visibility_of_element_located((By.ID, 'onetrust-accept-btn-handler')))
        time.sleep(1)
        accept_button.click()
        print("Accept button clicked.")
        time.sleep(1)
    except:
        pass


def scroll_and_click_more(driver, actions, target_class):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, target_class))
        )
        driver.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(1)
        element.click()
        print(f"Button with class {target_class} found and clicked.")
        return True
    except Exception as e:
        print(f"Error or button with class {target_class} not found: {e}")
        return False


def scrape_html(driver, filename):
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "css-14tfefh")))
    elements_in_product_list = element.find_elements(By.XPATH, ".//*")
    with open(filename, "w", encoding="utf-8") as file:
        for elem in elements_in_product_list:
            file.write(elem.get_attribute("outerHTML") + "\n")
    print(f"HTML output saved to {filename}.")


def main():
    driver = setup_driver()
    driver.get("https://www.carrefourksa.com/mafsau/en/c/FKSA1660000")
    actions = ActionChains(driver)

    accept_cookies(driver)

    # Scroll and click loop
    start_time = time.time()
    target_class = "css-10s9ah"
    max_duration = 480  # 8 minutes

    while time.time() - start_time < max_duration:
        loaded_new_content = scroll_and_click_more(driver, actions, target_class)
        if not loaded_new_content:
            break

    scrape_html(driver, "carrefourksa.txt")

    # Execute additional logic from output3
    Output3()

    # Clean up
    time.sleep(10)
    driver.quit()


if __name__ == "__main__":
    main()
