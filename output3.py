from bs4 import BeautifulSoup
import csv
import re
import chardet
from datetime import datetime, timedelta
import os


def Output3():
    
    PRODUCTS = []
    # Read the HTML content
    with open('carrefourksa.txt', 'rb') as file:
        result = chardet.detect(file.read())
        encoding = result['encoding']

    with open('carrefourksa.txt', 'r', encoding=encoding) as file:
        html_content = file.read()
    
    if html_content:

        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')
        product_details = soup.find_all('div', {'class': 'css-b9nx4o'})

        # Process each product
        for product in product_details:
            try:
                # Extract and process price
                price_text1 = product.find('div', {'class': 'css-14zpref'})
                price_text2 = product.find('div', {'class': 'css-1pjcwg4'})
                price = (price_text1.text.strip() if price_text1 else '') + (price_text2.text.strip() if price_text2 else '')

                # Extract and process currency
                currency_span = product.find('span', {'class': 'css-1edki26'})
                currency = currency_span.text.strip() if currency_span else 'SAR'

                # Extract and process product name
                product_name_a = product.find('a', {'data-testid': 'product_name'})
                full_product_name = product_name_a.text.strip() if product_name_a else product.find('div', {'class': 'css-1tmlydx'}).get_text(strip=True)
                weight_div = product.find('div', {'class': 'css-1tmlydx'})
                if weight_div:
                    weight_text = weight_div.get_text(strip=True)
                    weight_value = weight_text.split('-')[0].strip()
                else:
                    weight_value = ''

                # Extract name and amount
                match = re.search(r'(\D+)(\d.*)', full_product_name)
                if match:
                    name = match.group(1).strip().rstrip(',')
                    amount = match.group(2).strip().rstrip(',')
                else:
                    if weight_value:
                        amount = weight_value
                        name = full_product_name
                    else:
                        words = full_product_name.split()
                        if len(words) > 1:
                            amount = words[-1]
                            if amount == "pack":
                                name = ' '.join(words[:-1])
                            else:
                                name = ' '.join(words)
                                amount = 'count'
                        else:
                            name = words[0]
                            amount = ''

                # Extract offer price
                price_div = product.find('div', {'class': 'css-xj1pgi'})
                if price_div:
                    div_text = price_div.find('div', {'class': 'css-17fvam3'})
                    if div_text:
                        offer_price = div_text.get_text().split()[-1]
                        if offer_price:
                            numeric_part = re.search(r'\d+(?:\.\d+)?', offer_price).group()
                        else:
                            numeric_part = offer_price
                    else:
                        numeric_part = ''
                else:
                    numeric_part = ''
                # Collect product information
                iso_time = datetime.now().isoformat()
                # Convert the ISO time to Saudi Arabia time
                saudi_time_offset = timedelta(hours=3)  # Saudi Arabia is 3 hours ahead of UTC
                saudi_time = datetime.fromisoformat(iso_time) + saudi_time_offset
                item = {
                    'product_name': name,
                    'weight_unit': amount,
                    'official_price': numeric_part,
                    'offer_price': price,
                    'currency': currency,
                    'date': saudi_time.strftime('%Y-%m-%d'),
                    'from': 'http://www.carrefourksa.com'
                }
                if item not in PRODUCTS:
                    PRODUCTS.append(item)
            except Exception as e:
                print(f"An error occurred while processing a product: {e}")

        # Write to CSV
        with open("carrefourksa.csv", "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["Product Name", "Official Price", "Weight/Unit", "Offer Price", "Currency", "Date", "From"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for item in PRODUCTS:
                writer.writerow({
                    "Product Name": item["product_name"],
                    "Official Price": item["official_price"],
                    "Weight/Unit": item["weight_unit"],
                    "Offer Price": item["offer_price"],
                    "Currency": item["currency"],
                    "Date": item["date"],
                    "From": item["from"]
                })
        print("Data saved to carrfourksa.csv........")
        # file_name = 'carrefourksa.txt'
        # if os.path.exists(file_name):
        # # Remove the file
        #     os.remove(file_name)
        #     print(f"{file_name} has been deleted.")
    else:
        print("No HTML content foundt in the file.")


#  https://www.carrefourksa.com/mafsau/en/c/FKSA1660000