from seleniumbase import SB

with SB(uc=True, test=True,  incognito=True, locale_code="en") as sb:
    url = "https://aloqailat.com/en/category/DPndd"
    sb.uc_open_with_reconnect(url, reconnect_time=2)
    sb.uc_gui_handle_captcha()
    sb.uc_gui_click_captcha()  # Only if needed
    sb.sleep(4)
    # sb.assert_element("img#captcha-success", timeout=3)

    # Scroll down the page until an element with the specific class appears
    target_class = "testimonails-listing"
    sb.scroll_to_element(target_class, timeout=25)

    # Extract the data
    element = sb.find_element(By.CLASS_NAME, "products-grid")
    elements_in_product_list = element.find_elements(By.XPATH, ".//*")

    with open("aloqailat-1.txt", "w", encoding="utf-8") as file:
        for element in elements_in_product_list:
            file.write(element.get_attribute("outerHTML") + "\n")

    sb.set_messenger_theme(location="top_left")
    sb.post_message("SeleniumBase wasn't detected", duration=3)
