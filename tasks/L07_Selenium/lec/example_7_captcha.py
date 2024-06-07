import time
from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests

# Использование headless бразуреа, чтобы избежать механизмов обнаружения ботов
options = Options()
options.headless = True

# Создание экземпляра веб-драйвера
webdriver_service = service.Service("d:\\Prog\\WebDriver\\Opera\\operadriver.exe")
webdriver_service.start()

options = webdriver.ChromeOptions()
options.binary_location = "c:\\Program Files\\Opera\\opera.exe"
options.add_experimental_option('w3c', True)

driver = webdriver.Remote(webdriver_service.service_url, options=options)

# Загрузка веб-сайта
driver.get("https://www.example.com")

# Решение задачи CAPTCHA
captcha_element = driver.find_element(By.ID, "captcha")
captcha_image_src = captcha_element.get_attribute("src")
captcha_image_data = requests.get(captcha_image_src).content

# Использование OCR для извлечения текста из изображения CAPTCHA
captcha_text = "CAPTCHA_SOLUTION"

# Вывод текста CAPTCHA в форму
captcha_input = driver.find_element(By.ID, "captcha_input")
captcha_input.send_keys(captcha_text)

# Отправка формы
submit_button = driver.find_element(By.ID, "submit_button")
submit_button.click()

# Ожидание загрузки страницы после извлечения данных
time.sleep(3)

# Извлечение данных со страницы
data = driver.find_elements(By.XPATH, "//div[@class='data_element']")
data_list = []
for item in data:
    data_list.append(item.text)

# Закрытие веб-драйвера
driver.close()

# Вывод извлечённых данных
print(data_list)