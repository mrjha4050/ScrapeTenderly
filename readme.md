# Web Scraping eTenders

This Python script is designed to scrape tender information from the eTenders website (https://www.etenders.gov.za/Home/opportunities?id=1). It utilizes Selenium and BeautifulSoup libraries to extract data from the webpage.

## Requirements

- Python 3.x
- `requests`
- `beautifulsoup4`
- `selenium`
- `mysql-connector`
- Chrome WebDriver (Make sure it's compatible with your Chrome browser version)

## Installation


1. Install required libraries using pip:
    ```
    pip install requests beautifulsoup4 selenium mysql-connector
    ```

## Usage

1. Install Chrome WebDriver. Make sure it's in your system's PATH.
2. Run the Python script:
    ```
    python etender_scraper.py
    ```
4. Enter the starting page number when prompted.
5. The script will scrape tender data from the eTenders website and save it to a JSON file named `extracted_tenders.json`.
6. install my sql 
7. Run the python Script 
8. Run the python script:
    ```
    python db.py
    ```

## Additional Notes

- Ensure a stable internet connection as the script requires to access the eTenders website.
- Make sure Chrome WebDriver is compatible with your Chrome browser version. You may need to update WebDriver if you encounter issues.
- The script may take some time to execute depending on the number of pages to scrape.
# ScrapeTenderly
