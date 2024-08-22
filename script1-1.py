from selenium.webdriver.common.by import By
from seleniumbase import SB
from output2 import Output2

with SB(uc=True, test=True,  incognito=True, locale_code="en") as sb:
    url = "https://aloqailat.com/en/category/DPndd"
    sb.uc_open_with_reconnect(url, reconnect_time=2)
    sb.sleep(5)
    sb.uc_gui_handle_captcha()
    # sb.uc_gui_click_captcha()  # Only if needed
    sb.sleep(4)
    for _ in range(2):
            sb.scroll_to_bottom()
            sb.sleep(2)
        # Extract the data
    element = sb.find_element(By.CLASS_NAME, "products-grid")
    if element:
        elements_in_product_list = element.find_elements(By.XPATH, ".//*")

        with open("aloqailat-1.txt", "w", encoding="utf-8") as file:
            for element in elements_in_product_list:
                file.write(element.get_attribute("outerHTML") + "\n")
        sb.sleep(2)
        Output2("first")
        sb.sleep(5)
    else:
        sb.post_message("Element not found", duration=3)
    # sb.quit()
