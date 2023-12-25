import requests
from bs4 import BeautifulSoup
import json
import argparse
import os
import time

def fetch_page(product_name: str):
    """Fetch and parse HTML content of search result page from Amazon.ca for given product name"""
    product_name = product_name.replace(' ', '+') 
    url = f'https://www.amazon.ca/s?k={product_name}' 

    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0'})
    if response.status_code != 200: 
        raise Exception('Failed to get response')
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup 

def get_product_info(soup: BeautifulSoup):
    """Extract product names and their corresponding reviews"""
    all_products = soup.find_all('div', {'data-component-type': 's-search-result'}) 
    product_info = []
    for product in all_products:
        product_name = product.find('span', {'class': 'a-size-medium a-color-base a-text-normal'}).text
        product_reviews = product.find('span', {'class': 'a-size-base'}).text

        if product_name and product_reviews:
            product_info.append({
                'product_name': product_name, 
                'product_reviews': product_reviews
            })
    return product_info

if __name__ == '__main__':
    parser = argparse.ArgumentParser('description=Scrape Amazon products')
    parser.add_argument('-o', '--output_file', type=str, help='Output file name', required=True)
    args = parser.parse_args()

    products = ['water flosser', 'piano', 'weightlifting belt', 'basketball', 'guitar']

    all_products_info = []
    for product in products:
        soup = fetch_page(product)
        if soup:
            product_info = get_product_info(soup)
            all_products_info.append(product_info)
        time.sleep(3)

    output_path = os.path.join(os.path.dirname(__file__), '../data', args.output_file)

    with open(args.output_file, 'w') as f: 
        json.dump(all_products_info, f)