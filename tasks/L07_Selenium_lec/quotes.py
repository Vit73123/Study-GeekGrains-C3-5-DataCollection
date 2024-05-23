import csv

from selenium import webdriver
from selenium.webdriver.chrome import service

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import csv
import time
from pprint import pprint

webdriver_service = service.Service("d:\\Prog\\WebDriver\\Opera\\operadriver.exe")
webdriver_service.start()

options = webdriver.ChromeOptions()
options.binary_location = "c:\\Program Files\\Opera\\opera.exe"
options.add_experimental_option('w3c', True)

driver = webdriver.Remote(webdriver_service.service_url, options=options)

driver.get("http://quotes.toscrape.com/page/1/")

quotes = []

# if True:
while True:
    quote_elements = driver.find_elements(By.XPATH, "//div[@class='quote']")

    for quote_element in quote_elements:
        quote = quote_element.find_element(By.XPATH, ".//span[@class='text']").text
        author = quote_element.find_element(By.XPATH, ".//small[@class='author']").text
        quotes.append(
            {
                "quote": quote,
                "author": author
            }
        )

    try:
        next_button = driver.find_element(By.XPATH, "//li[@class='next']/a")
    except NoSuchElementException:
        break

    next_button.click()
    time.sleep(1)

driver.close()

# for quote in quotes:
#     print(quote["quote"], "by", quote["author"])

with open("quotes.csv", "w", newline="", encoding='UTF-8') as f:
    writer = csv.DictWriter(f, fieldnames=["quote", "author"])
    writer.writeheader()
    writer.writerows(quotes)