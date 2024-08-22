import requests
import csv
from datetime import datetime, timedelta
import time

PRODUCTS=[]
i=0
# Set the API endpoint URL
while(1):
    i=i+1
    url = f"https://shop.tamimimarkets.com/api/product?category=fruits--vegetables&layoutType=GRID&sorting=NEW_FIRST&page={i}"

    # Make the API request
    response = requests.get(url)

    # Check the response status code
    if response.status_code == 200:
        # The request was successful, get the data
        res = response.json()
        if "data" in res and "product" in res["data"] and res["data"]["product"] is not None:
            products = res["data"]["product"]
            for product in products:
                weight_unit =  product["variants"][0]["name"]
                official_price = round(float(product["variants"][0]["storeSpecificData"][0]["mrp"]),2)
                offer_price = round(official_price -  float(product["variants"][0]["storeSpecificData"][0]["discount"]), 2)
                currency = product["variants"][0]["storeSpecificData"][0]['currency']['name']
                iso_time = datetime.now().isoformat()
                # Convert the ISO time to Saudi Arabia time
                saudi_time_offset = timedelta(hours=3)  # Saudi Arabia is 3 hours ahead of UTC
                saudi_time = datetime.fromisoformat(iso_time) + saudi_time_offset
                item = {
                    'product_name': product["name"],
                    'weight_unit': weight_unit,
                    'official_price': official_price ,
                    'offer_price': offer_price,
                    'currency': currency,
                    'date': saudi_time.strftime('%Y-%m-%d'),
                    'from': 'shop.tamimimarkets.com'
                }
                if item not in PRODUCTS:
                 PRODUCTS.append(item)
        else:
            print("Scraping ended.")
            break
    else:
        # The request was not successful, handle the error
        print(f"Error: {response.status_code} - {response.text}")
    if i>50:
        print("break for infinity loop error.")
        break

 # Save the data to a CSV file
with open("tamimimarkets.csv", "w", newline="") as csvfile:
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
print('Data saved to tamimimarkets.csv ....')
time.sleep(2)
# https://shop.tamimimarkets.com/ar/category/fruits--vegetables