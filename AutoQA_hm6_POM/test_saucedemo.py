from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
import time

#  Были трудности с всплывающими окнами пришлось добавить больше пунктов и таймеров
#  чтобы понять сначала где код ломается а потом работает ли он штатно
firefox_options = Options()
firefox_options.add_argument("-private")
firefox_options.set_preference("dom.webnotifications.enabled", False)
firefox_options.set_preference("signon.rememberSignons", False)


firefox_options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
service = Service(r"C:\WebDriver\bin\geckodriver.exe")
driver = webdriver.Firefox(service=service, options=firefox_options)

try:
    WebDriverWait(driver, 5).until(lambda d: d.switch_to.alert)
    alert = driver.switch_to.alert
    print("⚠️ Закрываем алерт:", alert.text)
    alert.accept()  # или alert.dismiss() если нужно отклонить
except NoAlertPresentException:
    pass

try:
    login_page = LoginPage(driver)
    login_page.load()
    login_page.login("standard_user", "secret_sauce")

    inventory = InventoryPage(driver)
    inventory.add_item_to_cart("Sauce Labs Backpack")
    time.sleep(1)
    inventory.add_item_to_cart("Sauce Labs Bolt T-Shirt")
    time.sleep(1)
    inventory.add_item_to_cart("Sauce Labs Onesie")
    time.sleep(1)

    inventory.go_to_cart()
    time.sleep(1)

    cart_page = CartPage(driver)
    cart_page.click_checkout()
    time.sleep(1)

    checkout_page = CheckoutPage(driver)
    checkout_page.fill_form("Alex", "Titor", "10115")
    time.sleep(1)

    total_text = checkout_page.get_total()
    print("Найден Total:", total_text)

    assert "$58.29" in total_text, f"Ожидалось $58.29, получено {total_text}"

    input("Нажмите Enter")

finally:
    driver.quit()
