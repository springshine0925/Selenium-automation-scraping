from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
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
driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)

# Navigate to the Nintendo website
driver.get("https://www.sharbatly.club/collections/all")
wait = WebDriverWait(driver, 10)
form = wait.until(EC.visibility_of_element_located((By.ID, "locksmith-content")))
label_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='city-2']")))
label_element.click()
# print(driver.page_source)
time.sleep(2)

# element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "container.footer-menu-wrap")))
# # Scroll the element into view
# driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element)

# Scroll down the page until an element with the specific class appears
target_class = "footer"
start_time = time.time()

# Set the maximum duration of the loop (5 minutes = 300 seconds)
max_duration = 250

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
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Check if the target element reappears
    try:
        element = driver.find_element(By.CLASS_NAME, target_class)
        elapsed_time = time.time() - start_time
        # print("time==>",elapsed_time)
        # Check if 5 minutes have elapsed
        if elapsed_time >= max_duration:
            print("5 minutes have elapsed. Breaking the loop.")
            break
        if element.is_displayed():
            print("Element with class {} reappeared. Continuing scroll.".format(target_class))
        else:
            print("Element with class {} disappeared. Continuing scroll.".format(target_class))
    except:
        print("Element with class {} disappeared. Continuing scroll.".format(target_class))
        pass

element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "product-list")))

# product_list_div = driver.find_element_by_class_name("product-list")

# Find all elements within the div
elements_in_product_list = element.find_elements_by_xpath(".//*")

# Save the HTML code of the elements to a text file
with open("elements_html.txt", "w", encoding="utf-8") as file:
    for element in elements_in_product_list:
        file.write(element.get_attribute("outerHTML") + "\n")

# Close the browser session cleanly to free up system resources
driver.quit()



