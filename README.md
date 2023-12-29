# Amazon Web Scraping Project

#### Overview

- This project attempts to web scrape information from Amazon.ca's products, such as: product name, manufacturer, number of ratings, star rating, rating distribution, review rating and review content.

- The goal of this project is primarily to retrieve review contents to determine how many of the reviews may be botted.

- The motivation behind this project comes from a recent personal purchase of an Amazon.ca product that turned out being a disappointment despite high praise on the site.

#### TODO

- Web scrape first page of Amazon.ca products (by search), and each products' wanted information.

- Collect data, remove imperfections (incomplete data), and organize data in JSON format.

- Add a delay between request calls to avoid getting banned by Amazon.

- Use ML to identify if reviews are botted.

#### Notes

- Requests permission was denied (even with user agent), had to add Accepted-Languages.

- Added time.sleep() to add delay between calls to not get flagged.

- Added limit to number of products searched, to avoid getting max limit exceeded for request calls.

- Added a check to see if element was retrieved when getting product info; if not retrieved, return "NULL" instead.

#### Setup

- Run setup.sh found in scripts subdirectory to pip install all necessary dependencies.

#### Running

- Scrape: in terminal, run "python3 scraper.py --products "product1" "product2" "product3" -o output_file.json

  _Note that you may add as many products as desired_

- Machine learning:
