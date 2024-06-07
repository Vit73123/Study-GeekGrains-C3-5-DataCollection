from selenium import webdriver
from selenium.webdriver.chrome import service

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

webdriver_service = service.Service("d:\\Prog\\WebDriver\\Opera\\operadriver.exe")
webdriver_service.start()

options = webdriver.ChromeOptions()
options.binary_location = "c:\\Program Files\\Opera\\opera.exe"
options.add_experimental_option('w3c', True)

driver = webdriver.Remote(webdriver_service.service_url, options=options)

driver.get("https://www.imdb.com/chart/top")

movie_title_elemments = driver.find_elements(By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item h3")
rating_elements = driver.find_elements(By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item span.ipc-rating-star--imdb")

titles = [element.text for element in movie_title_elemments]
ratings = [element.text for element in rating_elements]

for i in range(10):
    print("Рейтинг {}: {} ({})".format(i + 1, titles[i], ratings[i]))

driver.quit()