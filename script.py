from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from output import Output
options = Options()
options.add_experimental_option("detach", True)

s = Service(f"chromedriver.exe")
DRIVER_PATH = 'chromedriver.exe'
prefs = {
  "translate_whitelists": {"ar":"en"},
  "translate":{"enabled":"true"}
}
options.add_argument("--lang=en")
options.add_experimental_option("prefs", prefs)
# Initialize Chrome with the specified options
service = Service(executable_path='./chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)
# driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)

# Navigate to the Nintendo website
driver.get("https://www.sharbatly.club/collections/all")
wait = WebDriverWait(driver, 10)
form = wait.until(EC.visibility_of_element_located((By.ID, "locksmith-content")))
label_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='city-2']")))
label_element.click()
time.sleep(2)

# Scroll down the page until an element with the specific class appears
target_class = "footer"
start_time = time.time()

# Set the maximum duration of the loop (5 minutes = 300 seconds)
max_duration = 180

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
    # Scroll down one page
    actions.send_keys(Keys.PAGE_DOWN).perform()
    # Scroll to the bottom of the page
    actions.send_keys(Keys.END).perform()

    # Check if the target element reappears
    try:
        element = driver.find_element(By.CLASS_NAME, target_class)
        elapsed_time = time.time() - start_time
        # Check if Time has elapsed
        if elapsed_time >= max_duration:
            print("Time has elapsed. Breaking the loop.")
            break
    except:
        print("Element with class {} disappeared. Continuing scroll.".format(target_class))
        pass

element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "product-list")))

# Find all elements within the div
# elements_in_product_list = element.find_elements_by_xpath(".//*")
elements_in_product_list = element.find_elements(By.XPATH, ".//*")


# Save the HTML code of the elements to a text file
with open("sharbatly.txt", "w", encoding="utf-8") as file:
    for element in elements_in_product_list:
        file.write(element.get_attribute("outerHTML") + "\n")

# Close the browser session cleanly to free up system resources
time.sleep(2)
Output()
time.sleep(10)

driver.quit()



