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

driver.get("https://www.amazon.com")

search_box = driver.find_element(By.ID, "twotabsearchtextbox")
search_box.send_keys("laptops")
search_box.submit()

assert "laptops" in driver.title

# div_element = driver.find_element(By.ID, "my-div")
# print(div_element.text)
# print(div_element.get_attribute("class"))

driver.quit()