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

driver.get("https://www.example.com")

driver.back()
driver.forward()
driver.refresh()
print(driver.title)
print(driver.current_url)

product = driver.find_element(By.XPATH, "//a[@href='/products/shirt")
product.click()

add_to_cart = driver.find_element(By.XPATH, "//button[text()='Добавить в корзину']")
add_to_cart.click()

cart_items = driver.find_element(By.XPATH, "//td[@class='cart-item-name']")

assert len(cart_items) == 1, "В корзине должен быть только 1 товар"
assert cart_items[0].text == "Рубашка", "В корзину добавлен неправильный товар"

driver.quit()