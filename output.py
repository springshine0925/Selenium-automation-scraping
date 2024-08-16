from bs4 import BeautifulSoup
import csv
import re
import chardet


def Output():

    PRODUCTS = []
    # Read the HTML content
    with open('sharbatly.txt', 'rb') as file:
        result = chardet.detect(file.read())
        encoding = result['encoding']

    with open('sharbatly.txt', 'r', encoding=encoding) as file:
        html_content = file.read()

    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        product_details = soup.find_all('div', {'class': 'product-details'})
        for product in product_details:
            product_name = product.find('span', {'class': 'title'}).text.strip()
            current_price = product.find('span', {'class': 'current_price'}).text.strip()
            was_price = product.find('span', {'class': 'was_price'}).text.strip()

            for i, char in enumerate(product_name):
                if char.isdigit() and char != "e":
                    break

            # Extract the name and amount
            name = product_name[:i].strip()
            if name.endswith(','):
                    name = name[:-1]
            amount = product_name[i:].strip()
            if amount.endswith(','):
                    amount = amount[:-1]

            pattern2 = r"(\d+\.\d+)\s(\w+)"
            match2 = re.match(pattern2, current_price)

            if match2:
                price1 = match2.group(1)
                currency1 = match2.group(2)
            else:
                price1 = ""
                currency1 = ""

            match3 = re.match(pattern2, was_price)

            if match3:
                price2 = match3.group(1)
                currency2 = match3.group(2)
            else:
                price2 = ""
                currency2 = ""

            item = {
                'product_name': name,
                'weight_unit': amount,
                'official_price': price2,
                'offer_price': price1,
                'currency': currency1
            }
            if item not in PRODUCTS:
                PRODUCTS.append(item)

        with open("sharbatly.csv", "w", newline="") as csvfile:
            fieldnames = ["Product Name", "Official Price", "Weight/Unit", "Offer Price", "Currency"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for item in PRODUCTS:
                writer.writerow({
                    "Product Name": item["product_name"],
                    "Official Price": item["official_price"],
                    "Weight/Unit": item["weight_unit"],
                    "Offer Price": item["offer_price"],
                    "Currency": item["currency"]
                })

                # https://www.sharbatly.club/collections/all
                # 
                #  https://www.sharbatly.club/ar

    else:
        print("input error for analysis.")


