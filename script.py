from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains
import time
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

s = Service(r"chromedriver.exe")
# Initialize Chrome with the specified options
driver = webdriver.Chrome(service=s, options=options)

# Navigate to the Nintendo website
driver.get("https://www.sharbatly.club/ar")
time.sleep(5)
# Output the page source to the console
action = ActionChains(driver)
test=driver.findElement(By.id("locksmith_passcode_form label"))
action.test.click()

action.perform()
print(driver.page_source)

# Close the browser session cleanly to free up system resources
# driver.quit()



