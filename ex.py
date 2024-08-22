import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions() 
options.headless = True
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = uc.Chrome(options=options)
driver.get('https://aloqailat.com/en/category/DPndd')
print(driver.find_element(By.XPATH, "/html/body").text)