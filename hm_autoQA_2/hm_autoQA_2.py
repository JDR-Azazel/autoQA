from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
import time


driver = webdriver.Firefox(service=Service())

try:
    driver.get("https://itcareerhub.de/ru")
    driver.maximize_window()
    time.sleep(15)


    payment_link = driver.find_element(By.LINK_TEXT, "Способы оплаты")
    payment_link.click()
    time.sleep(15)

    payment_section = driver.find_element(By.ID, "rec717852307")
    payment_section.screenshot("payments_section.png")

finally:
    driver.quit()
