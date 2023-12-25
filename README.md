# Amazon Web Scraping Project

1. This project attempts to web scrape amazon products and the content of their reviews, to determine how many of the reviews may be botted.

2. TODO : 
- Web scrape first page of amazon products (by search), and their reviews' contents.
- Collect data, remove imperfections, organize data. 
- Ensure to not get banned by Amazon for web scraping.
- Use ML to identify if reviews are botted.

3. Any surprises : 
- Requests permission was denied (even with user agent).

4. Setup/Installation : 
- Run setup.sh found in "scripts" sub-directory to install necessary dependencies.

5. Running : 
- Run "python3 scraper.py -o "output.json" to get products and their reviews.