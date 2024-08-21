from bs4 import BeautifulSoup
import csv
import re
import chardet
from datetime import datetime, timedelta
from googletrans import Translator
import os

def Output2(flag):
    if flag == "first":
        input_file = "aloqailat-1.txt"
        output_file = "aloqailat-1.csv"
    else:
        input_file = "aloqailat-2.txt"
        output_file = "aloqailat-2.csv"
    PRODUCTS = []

    with open(input_file, 'rb') as file:
        result = chardet.detect(file.read())
        encoding = result['encoding']
        print(f"Dectected encoding: {encoding}")

    with open(input_file, 'r', encoding=encoding) as file:
        html_content = file.read()
    if html_content:
        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')
        product_details = soup.find_all('div', {'class': 'product-box'})

        # Process each product
        translator = Translator()
        for product in product_details:
            try:
                # Extract and process price
                product_title = product.find('h3', {'class': 'product-title'}).get_text(strip=True)
                translation = translator.translate(product_title, src='ar', dest='en')
                product_title = translation.text

                if "by the kilo" in product_title or "per kilo" in product_title:
                    product_title = product_title.replace("by the kilo", "").replace("per kilo", "").strip()

                # Extract product price
                product_price = product.find('span', {'class': 'product-price'}).get_text(strip=True)
                translation1 = translator.translate(product_price, src='ar', dest='en')
                product_price = translation1.text
                price_currency = product_price.split()
                price = price_currency[0]
                currency = price_currency[1]
                # Collect product information
                iso_time = datetime.now().isoformat()
                    # Convert the ISO time to Saudi Arabia time
                saudi_time_offset = timedelta(hours=3)  # Saudi Arabia is 3 hours ahead of UTC
                saudi_time = datetime.fromisoformat(iso_time) + saudi_time_offset
                item = {
                    'product_name': product_title,
                    'weight_unit': "kilo or count",
                    'official_price': '',
                    'offer_price': price,
                    'currency': currency,
                    'date': saudi_time.strftime('%Y-%m-%d'),
                    'from': 'https://aloqailat.com'
                }
            
                if item not in PRODUCTS:
                    PRODUCTS.append(item)
            except Exception as e:
                print(f"An error occurred while processing a product: {e}")

        # Write to CSV
        with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
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
        print(f"Data saved to {output_file} .....")
        if os.path.exists(input_file):
        # Remove the file
            os.remove(input_file)
            print(f"{input_file} has been deleted.")
    else:
        print("No HTML content found in the file.")



# https://aloqailat.com/category/xymwG