from seleniumbase import BaseCase

class UndetectedTest(BaseCase):
    def test_browser_is_undetected(self):
        url = "https://aloqailat.com/en/category/DPndd"
        
        # Check if the browser is detectable
        if not self.undetectable:
            # If the browser is detectable, get a new undetectable driver
            self.get_new_driver(undetectable=True)
        
        # Open the website with automatic reconnection
        self.uc_open_with_reconnect(url, 4)
        
        # Handle the Cloudflare Turnstile challenge
        self.uc_gui_handle_captcha()
        self.sleep(5)
        
        # Verify the page content
        # self.assert_text("Username", '[for="user_login"]', timeout=3)
        self.post_message("SeleniumBase wasn't detected", duration=4)
        self._print("\n Success! Website did not detect Selenium!")

if __name__ == "__main__":
    UndetectedTest.main(__name__, __file__, "--uc", "-s")
