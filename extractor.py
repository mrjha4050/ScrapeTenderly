import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
from selenium.webdriver.common.by import By
import threading

stop_scraping = False

def listen_for_stop():
    global stop_scraping
    while True:
        command = input().lower()
        if command == "stop":
            stop_scraping = True
            print("Stopping the scraper...")
            break

scrape_all = input("Do you want to scrape all pages? (yes/no): ").lower()

if scrape_all == "no":
    starting_page = int(input("Enter the starting page number: "))
    ending_page = int(input("Enter the ending page number: "))
else:
    starting_page = 1
    ending_page = None  # No limit for ending page if scraping all pages

# URL to scrape
url = "https://www.etenders.gov.za/Home/opportunities?id=1"

# Open browser using Selenium
driver = webdriver.Chrome()
driver.get(url)
tenders = []

def getTableItems(current_page, ending_page):
    global stop_scraping
    while True:
        if stop_scraping:
            print("Scraping process stopped.")
            break

        time.sleep(20)  # Adjust time.sleep based on page load time

        table_body = driver.find_element(By.ID, "tendeList").find_element(
            By.TAG_NAME, "tbody"
        )

        for tr in table_body.find_elements(By.TAG_NAME, "tr"):
            tr.find_element(By.CLASS_NAME, "details-control").click()

        html = driver.page_source

        soup = BeautifulSoup(html, "html.parser")
        tender_table = soup.find(id="tendeList")

        if not tender_table:
            print("Tender table not found on this webpage.")
            return tenders

        def getNestTableData(tender_table):
            for row in tender_table.find_all(
                "tr",
                class_=lambda row_class: row_class
                and not row_class.startswith("details-controldetails-control"),
            ):
                tender_details = {}

                # Extract data from the row
                category_cell = row.find("td", class_="break-word")
                if category_cell:
                    tender_details["category"] = category_cell.text.strip()

                description_cell = row.find("td", class_="sorting_1")
                if description_cell:
                    tender_details["description"] = description_cell.text.strip()

                esubmission_cell = row.find("td", class_="text-center")
                if esubmission_cell:
                    esubmission_text = esubmission_cell.find(
                        "span", class_="esubnotAllowed"
                    )
                    if esubmission_text:
                        tender_details["eSubmission"] = "Not Allowed"
                    else:
                        tender_details["eSubmission"] = "Allowed"

                advertised_cell = row.find(
                    "td", string=lambda text: text and text.startswith("14/03/2024")
                )
                if advertised_cell:
                    tender_details["advertised_date"] = advertised_cell.text.strip()

                closing_cell = row.find(
                    "td", string=lambda text: text and "closing" in text.lower()
                )
                if closing_cell:
                    closing_text = closing_cell.text.strip().split("in ")
                    if len(closing_text) == 2:
                        tender_details["closing_date"] = closing_text[1]

                # Only extract nested data if key 'category' exists
                if "category" in tender_details:
                    details_table = soup.find(
                        "table", {"cellpadding": "5", "cellspacing": "0", "border": "0"}
                    )
                    if details_table:
                        rows = details_table.find_all("tr")
                        for row in rows:
                            cells = row.find_all("td")
                            if len(cells) == 2:
                                key = cells[0].text.strip().rstrip(":")
                                value = cells[1].text.strip()
                                tender_details[key] = value

                    tenders.append(tender_details)

        getNestTableData(tender_table)

        element = soup.find(id="tendeList_next")
        tabindex = element.get("tabindex")
        if tabindex != "-1" and (ending_page is None or current_page < ending_page):
            driver.find_element(By.ID, "tendeList_next").click()
            current_page += 1
        else:
            break

    return tenders

print("Scraping data .....")
time.sleep(3)
print("--------------------------------")   
print("If you want to stop write stop in the console.....")
stop_thread = threading.Thread(target=listen_for_stop)
stop_thread.start()

tenders = getTableItems(starting_page, ending_page)

json_data = json.dumps(tenders, indent=4)
with open("extracted_tenders.json", "w") as outfile:
    outfile.write(json_data)

print("Tender data saved to extracted_tenders.json")
driver.close()
