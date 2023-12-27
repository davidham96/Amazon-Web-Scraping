# Amazon Web Scraping Project

1. This project attempts to web scrape amazon products and the content of their reviews, to determine how many of the reviews may be botted.

2. TODO :

- Web scrape first page of amazon products (by search), and their reviews' contents.
- Collect data, remove imperfections, organize data.
- Ensure to not get banned by Amazon for web scraping.
- Use ML to identify if reviews are botted.

3. Any surprises/notes :

- Requests permission was denied (even with user agent), had to add Accepted-Languages.
- Added time.sleep() to add delay between calls to not get flagged.
- Instead of web scraping, used Amazon API (was blocked).

4. Setup/Installation :

- Run setup.sh found in "scripts" sub-directory to install necessary dependencies.

5. Running :
