import requests
from typing import TypedDict


class ProductReview(TypedDict):
    star_rating: float
    review_content: str


class ProductInfo(TypedDict):
    product_name: str
    manufacturer: str
    number_of_ratings: int
    review_distribution: dict
    reviews: list[ProductReview]
    average_rating: float


def product_id():
    return


def product_info():
    return


if __name__ == "__main__":
    pass
