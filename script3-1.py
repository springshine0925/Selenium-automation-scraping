from seleniumbase import BaseCase
import time
from output3 import Output3

class CarrefourScraper(BaseCase):
    def test_scrape_products(self):
        # Open the website
        self.open("https://www.carrefourksa.com/mafsau/en/c/FKSA1660000")
        self.sleep(4)
        # Accept cookies if the button is visible
        if self.is_element_visible("#onetrust-accept-btn-handler"):
            self.click("#onetrust-accept-btn-handler")
            print("Accept button clicked.")

        # Scroll and click the "More" button until it's no longer visible
        target_class = "css-10s9ah"
        start_time = time.time()
        max_duration = 400  # 8 minutes

        while time.time() - start_time < max_duration:
            try:
                self.wait_for_element_visible(".css-14tfefh")
                
                if self.is_element_visible(f".{target_class}"):
                    self.scroll_to(f".{target_class}")
                    self.sleep(2)
                    self.click(f".{target_class}")
                    print(f"Button with class {target_class} found and clicked.")
                    self.sleep(4)
                    self.wait_for_element_visible(".css-14tfefh")
                    self.sleep(3)
                else:
                    break
            except Exception as e:
                print(f"Error or button with class {target_class} not found: {e}") 
        # Scrape the product data
        self.sleep(3)
        filename= "carrefourksa.txt"
        # body =self.wait_for_element_visible("body")
        elements = self.find_elements(".css-14tfefh *")
        with open(filename, "w", encoding="utf-8") as file:
            for elem in elements:
                file.write(elem.get_attribute("outerHTML") + "\n")
        print(f"HTML output saved to {filename}.")
        self.sleep(1)
        Output3()
        self.sleep(5)
        # self.quit()
# if __name__ == "__main__":
#     from seleniumbase import run
#     run(CarrefourScraper)