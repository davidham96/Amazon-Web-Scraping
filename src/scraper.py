import requests
from bs4 import BeautifulSoup
import json
import argparse
import os

def fetch_product(product_name: str):
    """
    Fetch and parse HTML content of search result page from Amazon.ca for given products
    Takes a product name string as input, and returns BeautifulSoup object with parsed HTML content
    """

    product_name = product_name.replace(' ', '+') # replace spaces with + for url
    url = f'https://www.amazon.ca/s?k={product_name}' # url to scrape

    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0'})
    if response.status_code != 200: 
        raise Exception('Failed to get response')
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup   

def get_product_info(soup: BeautifulSoup):
    """
    Extracts all products on first page, and product information from BeautifulSoup object
    Takes soup object as input, and returns list of info for given product
    """

    all_products = soup.find_all('div', {'data-component-type': 's-search-result'}) # get all products on first page
    # TODO: fix soup.find_all...
    results = []
    for product in all_products:
        product_name = product.find('span', {'class': 'a-size-medium a-color-base a-text-normal'}).text
        # TODO: fix product.find...
        # TODO: get more product information
        results.append(product_name)
    return results

if __name__ == '__main__':
    parser = argparse.ArgumentParser('description=Scrape Amazon products')
    parser.add_argument('-o', '--output_file', type=str, help='Output file name', required=True)
    args = parser.parse_args()

    products_list = ['water flossers', 'piano', 'weightlifting belt', 'basketball', 'guitar']

    all_products_info = []
    for product in products_list:
        soup = fetch_product(product)
        if soup:
            product_info = get_product_info(soup)
            all_products_info.append(product_info)

    output_path = os.path.join(os.path.dirname(__file__), '../data', args.output_file)

    with open(args.output_file, 'w') as f: # write to json file
        json.dump(all_products_info, f)