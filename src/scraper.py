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
    return BeautifulSoup(response.content, "html.parser")


def get_products(soup: BeautifulSoup) -> list:
    """Get products from search result page and call get_product_info"""
    all_products = soup.find("div", {"class": "s-result-list"}).find_all(
        "div", {"data-component-type": "s-search-result"}
    )
    product_info = []
    limit = 1
    count = 0
    for product in all_products:
        if count == limit:
            break
        product_link = "amazon.ca" + product.find("a")["href"]
        product_info.append((get_product_info(product_link)))
        count += 1
    return product_info


class ProductReview(TypedDict):
    rating: float
    content: str


class ProductInfo(TypedDict):
    product_name: str
    manufacturer: str
    number_of_ratings: int
    star_rating: float
    rating_distribution: dict
    reviews: list[ProductReview]


def get_element(element):
    return element.text if element else "NULL"


def get_product_info(product_link: str) -> ProductInfo:
    """Get product info from product page"""
    product_link = "https://" + product_link
    print("Visiting: " + product_link + " ...")
    time.sleep(5)
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

    product_name = get_element(soup.find("span", {"id": "productTitle"})).strip()

    technical_table_contents = soup.find(
        "table", {"id": "productDetails_techSpec_section_1"}
    )
    additional_table_contents = soup.find("div", {"id": "productDetails_db_sections"})
    all_elements = []
    if technical_table_contents:
        all_elements = technical_table_contents.find_all("tr")
    if additional_table_contents:
        all_elements += additional_table_contents.find_all("tr")
    for row in all_elements:
        manufacturer = get_element(row.find("th")).strip()
        if "manufacturer" in manufacturer.lower() and " " not in manufacturer:
            manufacturer = get_element(row.find("td")).strip()
            break

    number_of_ratings = (
        get_element(soup.find("span", {"id": "acrCustomerReviewText"}))
        .strip()
        .split(" ")[0]
    )
    star_rating = (
        get_element(soup.find("span", {"class": "a-size-medium a-color-base"}))
        .strip()
        .split(" ")[0]
    )

    rating_distribution = {}
    all_stars = soup.find_all("tr", {"class": "a-histogram-row"})
    x = 5
    for star in all_stars:
        rating_distribution[x] = get_element(
            star.find("td", {"class": "a-text-right"})
        ).strip()
        x -= 1

    product_id = response.url.split("/dp/")[1].split("/")[0]
    reviews = []
    page = 1
    while True:
        page_reviews = get_review_info(product_id, page)
        if not page_reviews:
            break
        reviews.append(page_reviews)
        page += 1
        time.sleep(5)

    return {
        "Product Name": product_name,
        "Manufacturer": manufacturer,
        "Number of Ratings": number_of_ratings,
        "Star Rating": star_rating,
        "Rating Distribution": rating_distribution,
        "Reviews": reviews,
    }


def get_review_info(product_id: str, page: int) -> list[ProductReview]:
    """Get review info from each review page"""
    review_page_url = f"https://www.amazon.ca/product-reviews/{product_id}/ref=cm_cr_getr_d_paging_btm_next_{page}?pageNumber={page}"
    print("Visiting: " + review_page_url + " ...")
    time.sleep(5)

    response = requests.get(
        review_page_url,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Accepted-Language": "en-CA,en-US;q=0.7,en;q=0.3",
        },
    )
    if response.status_code != 200:
        raise Exception("Failed to get response: " + response.text)
    soup = BeautifulSoup(response.content, "html.parser")

    reviews = []
    reviews_table = soup.find("div", {"id": "cm_cr-review_list"})
    all_reviews = reviews_table.find_all("div", {"data-hook": "review"})

    if not all_reviews:
        return reviews

    for review in all_reviews:
        review_rating_location = review.find("i", {"class": "review-rating"})
        if not review_rating_location:
            continue
        review_rating = get_element(
            review_rating_location.find("span", {"class": "a-icon-alt"})
        ).split(" ")[0]
        review_content = get_element(
            review.find("span", {"data-hook": "review-body"})
        ).strip()
        reviews.append({"Rating": review_rating, "Content": review_content})

    return reviews


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--products", nargs="+", required=True)
    parser.add_argument("-o", "--output_file", type=str, required=True)
    args = parser.parse_args()

    all_products_info = []
    for product in args.products:
        soup = get_search_page(product)
        if soup:
            product_info = get_products(soup)
            all_products_info.append(product_info)
        time.sleep(5)

    output_path = os.path.join(os.path.dirname(__file__), "../data", args.output_file)

    with open(output_path, "w") as f:
        json.dump(all_products_info, f)
