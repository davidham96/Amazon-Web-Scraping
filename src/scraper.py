import requests
from bs4 import BeautifulSoup
import json
import argparse
import os
import time
from typing import TypedDict


def get_search_page(product_name: str) -> BeautifulSoup:
    """Fetch and parse HTML content of search result page from Amazon.ca for given product name"""
    product_name = product_name.replace(" ", "+")
    url = f"https://www.amazon.ca/s?k={product_name}"

    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Accepted-Language": "en-CA,en-US;q=0.7,en;q=0.3",
        },
    )

    if response.status_code != 200:
        raise Exception("Failed to get response: " + response.text)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


def get_products(soup: BeautifulSoup) -> list:
    all_products = soup.find("div", {"class": "s-result-list"}).find_all(
        "div", {"data-component-type": "s-search-result"}
    )
    product_info = []
    for product in all_products:
        product_link = "amazon.ca" + product.find("a")["href"]
        product_info.append((get_product_info(product_link)))
    return product_info


class ProductReview(TypedDict):
    star_rating: float
    review_content: str


class ProductInfo(TypedDict):
    product_name: str
    manufacturer: str
    number_of_ratings: int
    star_rating: float
    rating_distribution: dict
    reviews: list[ProductReview]


def get_product_info(product_link: str) -> ProductInfo:
    product_link = "https://" + product_link
    print("Visiting: " + product_link + " ...")
    time.sleep(2)
    response = requests.get(
        product_link,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Accepted-Language": "en-CA,en-US;q=0.7,en;q=0.3",
        },
    )

    if response.status_code != 200:
        raise Exception("Failed to get response: " + response.text)
    soup = BeautifulSoup(response.content, "html.parser")

    def get_element(element):
        return element.text if element else "NULL"

    product_name = get_element(soup.find("span", {"id": "productTitle"})).strip()
    manufacturer = get_element(soup.find("td", {"class": "a-size-base"})).strip()
    number_of_ratings = (
        get_element(soup.find("span", {"id": "acrCustomerReviewText"}))
        .strip()
        .split(" ")[0]
    )
    star_rating = get_element(
        soup.find("span", {"class": "a-size-base a-color-base"})
    ).strip()

    rating_distribution = {}
    all_stars = soup.find_all("tr", {"class": "a-histogram-row"})
    x = 5
    for star in all_stars:
        rating_distribution[x] = get_element(
            star.find("td", {"class": "a-text-right"})
        ).strip()
        x -= 1

    return {
        "Product Name": product_name,
        "Manufacturer": manufacturer,
        "Number of Ratings": number_of_ratings,
        "Star Rating": star_rating,
        "Rating Distribution": rating_distribution,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser("description=Scrape Amazon products")
    parser.add_argument("--products", nargs="+", required=True)
    parser.add_argument(
        "-o", "--output_file", type=str, help="Output file name", required=True
    )
    args = parser.parse_args()

    all_products_info = []
    for product in args.products:
        soup = get_search_page(product)
        if soup:
            product_info = get_products(soup)
            all_products_info.append(product_info)
        time.sleep(2)

    output_path = os.path.join(os.path.dirname(__file__), "../data", args.output_file)

    with open(output_path, "w") as f:
        json.dump(all_products_info, f)
