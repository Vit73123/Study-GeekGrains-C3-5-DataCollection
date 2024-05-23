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

driver.get("https://www.example.com/movies")

next_button_locator = (By.XPATH, "//a[@class='next']")

current_page = 1
while True:
    print(f"Scraping page {current_page}...")

    try:
        next_button = driver.find_element(*next_button_locator)
        next_button.click()
        current_page += 1
    except NoSuchElementException:
        break

driver.quit()