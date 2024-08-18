from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from output3 import Output3

options = Options()
options.add_experimental_option("detach", True)

prefs = {
  "translate_whitelists": {"ar":"en"},
  "translate":{"enabled":"true"}
}
options.add_argument("--lang=en")
options.add_experimental_option("prefs", prefs)

# Initialize Chrome with the specified options
service = Service(executable_path='./chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)

def main():
    # Navigate to the Carrefour KSA website
    driver.get("https://www.carrefourksa.com/mafsau/en/c/FKSA1660000")
    wait = WebDriverWait(driver, 10)

    # Scroll down the page until an element with the specific class appears
    target_class = "css-10s9ah"
    start_time = time.time()
    time.sleep(10)

    # Check and click the accept button if it appears
    try:
        accept_button = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
        if accept_button:
            accept_button.click()
            print("Accept button clicked.")
            time.sleep(1)
    except:
        pass

    # Set the maximum duration of the loop (3 minutes = 180 seconds)
    max_duration = 180
    actions = ActionChains(driver)

    while True:
        # Scroll down the page slowly
        while True:  
            current_scroll_position = driver.execute_script("return window.pageYOffset + window.innerHeight;")
            total_scroll_height = driver.execute_script("return document.body.scrollHeight;")
            if current_scroll_position >= total_scroll_height:
                print("Reached the bottom of the page.")
                break
            else:
                pass
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, target_class))
                )
                if element:
                    time.sleep(3)
                    element.click()
                    print(f"Button with class {target_class} found and clicked.")
                    time.sleep(10)
                    # break
            except:
                print(f"Button with class {target_class} not found. Continuing scroll.")
                pass
            actions.send_keys(Keys.ARROW_DOWN).perform()
            time.sleep(0.3)  

        # Scroll up the page slowly
        while True:  # Adjust the range for finer control
            current_scroll_position = driver.execute_script("return window.pageYOffset + window.innerHeight;")
            total_scroll_height = driver.execute_script("return document.body.scrollHeight;")
            if current_scroll_position == 0:
                print("Reached the top of the page.")
                break
            try:
                actions.send_keys(Keys.ARROW_UP).perform()
                time.sleep(0.1)  # Short delay for smoother scrolling
                # Check if at the top of the page
                current_scroll_position = driver.execute_script("return window.pageYOffset;")
            except Exception as e:
                print(f"Error while scrolling up: {e}")
                # break

        # Check if the maximum duration has elapsed
        elapsed_time = time.time() - start_time
        if elapsed_time >= max_duration:
            print("Maximum duration reached. Breaking the loop.")
            break

    # Continue with the rest of your script
    element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "css-14tfefh")))

    # Find all elements within the div
    elements_in_product_list = element.find_elements(By.XPATH, ".//*")

    # Save the HTML code of the elements to a text file
    with open("carrefourksa.txt", "w", encoding="utf-8") as file:
        for elem in elements_in_product_list:
            file.write(elem.get_attribute("outerHTML") + "\n")

    # Close the browser session cleanly to free up system resources
    time.sleep(2)
    Output3()
    time.sleep(10)
    driver.quit()

if __name__ == "__main__":
    main()