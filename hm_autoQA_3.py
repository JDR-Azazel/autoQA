"""
Написать автотест с использованием Python и Pytest, который:
1. Открывает https://itcareerhub.de/ru
2. Проверяет, что на странице отображаются:
- Логитип ITCareerHub
- Ссылка “Программы”
- Ссылка “Способы оплаты”
- Ссылка “Новости”
- Ссылка “О нас”
- Ссылка “Отзывы”
- Кнопки переключения языка (ru и de)

3. Кликнуть по иконке с телефонной трубкой
4. Проверить что текст “Если вы не дозвонились, заполните форму на сайте. Мы свяжемся с вами” отображается.
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


@pytest.fixture
def driver():
    service = Service()
    driver = webdriver.Firefox(service=service)
    yield driver
    driver.quit()

#1. Открывает https://itcareerhub.de/ru
def test_itcareerhub_homepage_with_clicks(driver):
    driver.get("https://itcareerhub.de/ru")
    wait = WebDriverWait(driver, 10)

    # Проверка логотипа ITCareerHub
    logo = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "img.tn-atom__img")))
    assert logo.is_displayed()

    # Проверка ссылок с кликами
    menu_links = ["Программы", "Способы оплаты", "Новости", "О нас", "Отзывы", "Контакты"]

    for text in menu_links:
        link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, text)))
        main_window = driver.current_window_handle
        link.click()
        time.sleep(1)


        if len(driver.window_handles) > 1:
            new_window = [h for h in driver.window_handles if h != main_window][0]
            driver.switch_to.window(new_window)
            time.sleep(1)
            driver.close()
            driver.switch_to.window(main_window)
        else:
            driver.back()


        wait.until(EC.presence_of_element_located((By.LINK_TEXT, text)))

    # Проверка кнопок переключения языка (ru и de)
    lang_buttons = ["ru", "de"]
    for lang in lang_buttons:
        button = driver.find_element(By.LINK_TEXT, lang)
        assert button.is_displayed(), f"Кнопка языка '{lang}' не найдена"

    # Ищем иконку с телефонной трубкой
    phone_icon = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="#popup:form-tr3"] img'))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", phone_icon)
    time.sleep(1)
    phone_icon.click()

    # Проверяем текст после клика
    text_element = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[contains(text(), 'Если вы не дозвонились, заполните форму на сайте. Мы свяжемся с вами')]")
        )
    )
    assert text_element.is_displayed()
