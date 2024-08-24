from seleniumbase import BaseCase
import time
from output3 import Output3
BaseCase.main(__name__, __file__)

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
        max_duration = 300 

        while time.time() - start_time < max_duration:
            try:
                self.wait_for_element_visible(".css-14tfefh")
                # self.wait_for_element_visible(f".{target_class}")
                
                # if self.is_element_visible(f".{target_class}"):
                if self.wait_for_element_visible(f".{target_class}"):
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
        print("Time out....")
        self.sleep(5)
        filename= "carrefourksa.txt"
        target_div = self.wait_for_element_visible("css selector", ".css-33yiqn")
        elements_in_div = self.find_elements("css selector", ".css-33yiqn *")
        self.sleep(2)
        with open(filename, "w", encoding="utf-8") as file:
            for element in elements_in_div:
                file.write(element.get_attribute("outerHTML") + "\n")
        print(f"HTML output saved to {filename}.")
        self.sleep(1)
        Output3()
        self.sleep(5)
        # self.quit()
# if __name__ == "__main__":
#     from seleniumbase import run
#     run(CarrefourScraper)