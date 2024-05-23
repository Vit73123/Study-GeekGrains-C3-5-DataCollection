import csv

from selenium import webdriver
from selenium.webdriver.chrome import service

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

webdriver_service = service.Service("d:\\Prog\\WebDriver\\Opera\\operadriver.exe")
webdriver_service.start()

options = webdriver.ChromeOptions()
options.binary_location = "c:\\Program Files\\Opera\\opera.exe"
options.add_experimental_option('w3c', True)

driver = webdriver.Remote(webdriver_service.service_url, options=options)

driver.get("https://duckduckgo.com")

# Поиск строки поиска и ввод поискового запроса
search_bar = driver.find_element(By.NAME, "q")
search_bar.send_keys("Selenium blocks")

# Поиск кнопки поиска и нажатие на неё
search_button = driver.find_element(By.XPATH, "//button[@type='submit']")
search_button.click()

# Поиск выпадающего меню "Время" и щелчок по нему
time_dropdown = driver.find_element(By.XPATH, "//*[@id='links_wrapper']/div[1]/div/div/div[3]/a")
time_dropdown.click()

# Поиск опции "За последний мисеяц" в выпадающем меню времени и щелчок по ней
time_last_month = driver.find_element(By.XPATH, "*//a[@data-value='m']")
time_last_month.click()

more_bin = driver.find_element(By.XPATH, "//button[@id='more-results']")
more_bin.click()

# Поиск всех результатов на странице
results = driver.find_elements(By.XPATH, "//h2[@class='LnpumSThxEWMIsDdAT17 CXMyPcQ6nDv47DKFeywM']")
result_data = []

# Извлечение заголовка и URL каждого результата
for result in results:
    result_title = result.find_element(By.XPATH, ".//a[@class='eVNpHGjtxRBq_gLOfGDr LQNqh2U1kzYxREs65IJu']").text
    result_url = result.find_element(By.XPATH, ".//a[@class='eVNpHGjtxRBq_gLOfGDr LQNqh2U1kzYxREs65IJu']").get_attribute("href")

    result_data.append([result_title, result_url])

driver.close()

# Запись данных в CSV
with open("duckduckgo.csv", "w", newline="", encoding="UTF-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Result Title", "URL"])
    writer.writerows(result_data)