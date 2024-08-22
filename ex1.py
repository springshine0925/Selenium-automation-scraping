from seleniumbase import SB

with SB(uc=True, test=True, locale_code="en") as sb:
    url = "https://aloqailat.com/en/category/DPndd"
    # input_field = 'input[placeholder="Enter domain"]'
    submit_button = 'span:contains("Verify you are human")'
    sb.driver.uc_open_with_reconnect(url, 1)  # The bot-check is later
    # sb.type(input_field, "github.com/seleniumbase/SeleniumBase")
    sb.driver.reconnect(0.1)
    sb.driver.uc_click(submit_button, reconnect_time=4)
    sb.wait_for_text_not_visible("Verifying...", timeout=10)
    # sb.highlight('p:contains("github.com/seleniumbase/SeleniumBase")')
    # sb.highlight('a:contains("Top 100 backlinks")')
    sb.set_messenger_theme(location="bottom_center")
    sb.post_message("SeleniumBase wasn't detected!")
                