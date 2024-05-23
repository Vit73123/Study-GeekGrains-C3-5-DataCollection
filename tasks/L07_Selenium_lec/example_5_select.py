from selenium import webdriver
from selenium.webdriver.chrome import service

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

webdriver_service = service.Service("d:\\Prog\\WebDriver\\Opera\\operadriver.exe")
webdriver_service.start()

options = webdriver.ChromeOptions()
options.binary_location = "c:\\Program Files\\Opera\\opera.exe"
options.add_experimental_option('w3c', True)

driver = webdriver.Remote(webdriver_service.service_url, options=options)

driver.get("https://www.example.com/dropdown-menu")

# Найдите выпадающее меню и выберите нужную опцию
dropdown = driver.find_element(By.ID, "dropdown-menu")
select = Select(dropdown)
select.select_by_visible_text("Option 2s")

driver.close()
