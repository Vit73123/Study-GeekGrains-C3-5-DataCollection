from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

webdriver_service = service.Service("d:\\Prog\\WebDriver\\Opera\\operadriver.exe")
webdriver_service.start()

options = webdriver.ChromeOptions()
options.binary_location = "c:\\Program Files\\Opera\\opera.exe"
options.add_experimental_option('w3c', True)
options.add_argument('start-maximized')

driver = webdriver.Remote(webdriver_service.service_url, options=options)

driver.get("https://www.wildberries.ru")

time.sleep(2)
input = driver.find_element(By.ID, "searchInput")
input.send_keys("телевизор dexp 32")
input.send_keys(Keys.ENTER)

time.sleep(3)
scroll_count = 0

goods = []
while True:
    while True:
        wait = WebDriverWait(driver, 30)
        cards = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//article[@id]")))

        # cards = driver.find_elements(By.XPATH, "//article[@id]")    # 100
        count = len(cards)
        driver.execute_script("window.scrollBy(0, 1000)")
        time.sleep(1)
        cards = driver.find_elements(By.XPATH, "//article[@id]")  # ? == 100

        if len(cards) == count:
            if scroll_count == 3:
                break
            else:
                scroll_count += 1
        else:
            scroll_count = 0

        # if len(cards) == count:
        #     break

    for card in cards:
        price = card.find_element(By.CLASS_NAME, "price__lower-price").text
        name = card.find_element(By.XPATH, "./div/a").get_attribute('aria-label')
        url = card.find_element(By.XPATH, "./div/a").get_attribute('href')
        goods.append(
            {
                'price': price,
                'name': name,
                'url': url,
            }
        )
        print(name, price, url)
        # TODO: save to database

    try:
        button = driver.find_element(By.CLASS_NAME, 'pagination-next')
        # actions = ActionChains(driver)
        # actions.scroll_to_element(button).click()    # .key_down(Keys.CONTROL).key_down(Keys.C)
        # actions.move_to_element(button).click()
        # actions.perform()
        button.click()
    except:
        break

print()

driver.close()
