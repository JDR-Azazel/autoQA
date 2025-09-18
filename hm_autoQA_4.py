"""
Задание 1: Проверка изменения текста кнопки
Тестируемый сайт:
http://uitestingplayground.com/textinput

Шаги теста:
    1. Перейдите на сайт Text Input.
    2. Введите в поле ввода текст "ITCH".
    3. Нажмите на синюю кнопку.
    4. Проверьте, что текст кнопки изменился на "ITCH".

Задание 2: Проверка загрузки изображений
Тестируемый сайт:
https://bonigarcia.dev/selenium-webdriver-java/loading-images.html

Шаги теста:
    1. Перейдите на сайт Loading Images.
    2. Дождитесь загрузки всех изображений.
    3. Получите значение атрибута alt у третьего изображения.
    4. Убедитесь, что значение атрибута alt равно "award".
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    driver = webdriver.Firefox()
    driver.maximize_window()
    yield driver
    driver.quit()


# Задание 1: Проверка изменения текста кнопки
def test_text_input_button_change(driver):
    driver.get("http://uitestingplayground.com/textinput")
    wait = WebDriverWait(driver, 10)

    # Ввод текста
    input_field = wait.until(EC.presence_of_element_located((By.ID, "newButtonName")))
    input_field.clear()
    input_field.send_keys("ITCH")

    # Нажатие кнопки
    button = wait.until(EC.element_to_be_clickable((By.ID, "updatingButton")))
    button.click()

    # Проверка текста кнопки
    assert button.text == "ITCH", f"Ожидалось 'ITCH', но получили '{button.text}'"


# Задание 2: Проверка загрузки изображений
def test_loading_images_alt_text(driver):
    driver.get("https://bonigarcia.dev/selenium-webdriver-java/loading-images.html")
    wait = WebDriverWait(driver, 15)

    # Чтобь убедится что все прогрузилось вместо таймера ожидаю появления надписи
    wait.until(EC.text_to_be_present_in_element((By.ID, "text"), "Done!"))

    images = driver.find_elements(By.CSS_SELECTOR, "img")

    # Тут два варианта исключить логотип либо искать 3 индекс элемента а не второй как ниже чтобы он был действительно award
    content_images = [img for img in images if "hands-on-icon.png" not in img.get_attribute("src")]

    # Получаем alt третьей подгруженной картинки
    third_img_alt = content_images[2].get_attribute("alt")
    assert third_img_alt == "award", f"Ожидалось 'award', но получили '{third_img_alt}'"
