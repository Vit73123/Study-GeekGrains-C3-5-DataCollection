from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import csv

import locale
from datetime import datetime, timedelta
from dateutil.parser import parse
from pprint import pprint
import time

news = []
MAX_NEWS_COUNT = 25

webdriver_service = service.Service("d:\\Prog\\WebDriver\\Opera\\operadriver.exe")
webdriver_service.start()

options = webdriver.ChromeOptions()
options.binary_location = "c:\\Program Files\\Opera\\opera.exe"
options.add_experimental_option('w3c', True)
options.add_argument('start-maximized')

driver = webdriver.Remote(webdriver_service.service_url, options=options)

locale.setlocale(locale.LC_ALL, 'ru')
MONTHS = {
    "января": 1,
    "февраля": 2,
    "марта": 3,
    "апреля": 4,
    "мая": 5,
    "июня": 6,
    "июля": 7,
    "августа": 8,
    "сентября": 9,
    "октября": 10,
    "ноября": 11,
    "декабря": 12,
}


def to_date(s: str):
    *date, time = s.split(", ")
    time = parse(time).time()
    today = datetime.now().date()
    if date:
        day, *month = date[0].split()
        if month:
            month = MONTHS[month[0].lower()]
            day = datetime(today.year, month, int(day)).date()
        elif day.lower() == 'вчера':
            day = today - timedelta(days=1)
    else:
        day = today
    return datetime.combine(day, time)


if __name__ == "__main__":
    driver.get("https://ria.ru/lenta/")
    time.sleep(1)

    count = 0

    while True:
        wait = WebDriverWait(driver, 30)
        items = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='list-item']")))

        driver.execute_script("window.scrollBy(0, 10000)")

        if count == 0:
            button = driver.find_element(By.CSS_SELECTOR, "div.list-more")
            actions = ActionChains(driver)
            actions.move_to_element(button).click()
            actions.perform()
        elif count == len(items):
            break

        for item in items:
            if count == MAX_NEWS_COUNT:
                break
            else:
                count += 1

            title = item.find_element(By.CSS_SELECTOR, "a.list-item__title").text
            date_time = to_date(item.find_element(By.XPATH, ".//div[@class='list-item__date']").text)
            url = item.find_element(By.CSS_SELECTOR, "a.list-item__title").get_attribute('href')

            news.append(
                {
                    'title': title,
                    'date_time': date_time,
                    'url': url
                }
            )

        if count == MAX_NEWS_COUNT:
            break

    with open('news.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["title", "date_time", "url"])
        for item in news:
            writer.writerow([item['title'], item['date_time'], item['url']])
    print()

    driver.close()
