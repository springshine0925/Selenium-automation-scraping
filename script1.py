from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from output2 import Output2
# from seleniumbase import SB

# with SB(uc=True, test=True) as sb:
#     url = ""
options = Options()
options.add_experimental_option("detach", True)

# s = Service(f"chromedriver.exe")
# DRIVER_PATH = 'chromedriver.exe'
prefs = {
  "translate_whitelists": {"ar":"en"},
  "translate":{"enabled":"true"}
}
options.add_argument("--lang=en")
options.add_experimental_option("prefs", prefs)
service = Service(executable_path='./chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)

# Navigate to the Nintendo website
driver.get("https://aloqailat.com/en/category/DPndd")
time.sleep(10)
wait = WebDriverWait(driver, 10)
chapcha_div = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'spacer')))
chapcha_check = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='checkbox]")))
chapcha_check.click()
time.sleep(5)
# Scroll down the page until an element with the specific class appears
target_class = "testimonails-listing"
start_time = time.time()

# Set the maximum duration of the loop (5 minutes = 300 seconds)
max_duration = 25

while True:
    # Scroll down the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Check if the target element is visible
    try:
        element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, target_class)))
        print("Element with class {} found. Scrolling stopped.".format(target_class))
        break
    except:
        pass

# If the element is no longer visible, continue scrolling down
while True:
    # Scroll down the page
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    actions = ActionChains(driver)
    actions.send_keys(Keys.PAGE_DOWN).perform()
    actions.send_keys(Keys.END).perform()
    # Check if the target element reappears
    try:
        element = driver.find_element(By.CLASS_NAME, target_class)
        elapsed_time = time.time() - start_time
        # Check if 5 minutes have elapsed
        if elapsed_time >= max_duration:
            print("Time has elapsed. Breaking the loop.")
            break
    except:
        print("Element with class {} disappeared. Continuing scroll.".format(target_class))
        pass

element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "products-grid")))

elements_in_product_list = element.find_elements(By.XPATH, ".//*")

# Save the HTML code of the elements to a text file
with open("aloqailat-1.txt", "w", encoding="utf-8") as file:
    for element in elements_in_product_list:
        file.write(element.get_attribute("outerHTML") + "\n")

# Close the browser session cleanly to free up system resources
time.sleep(2)
Output2("first")
time.sleep(5)

driver.quit()



