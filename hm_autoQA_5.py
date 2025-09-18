"""
Задание 1: Проверка наличия текста в iframe
Открыть страницу
Перейти по ссылке: https://bonigarcia.dev/selenium-webdriver-java/iframes.html.

Проверить наличие текста
- Найти фрейм (iframe), в котором содержится искомый текст.
- Переключиться в этот iframe.
- Найти элемент, содержащий текст "semper posuere integer et senectus justo curabitur.".
- Убедиться, что текст отображается на странице.

Задание 2: Тестирование Drag & Drop (Перетаскивание изображения в корзину)
Открыть страницу Drag & Drop Demo.
Перейти по ссылке: https://www.globalsqa.com/demo-site/draganddrop/.

Выполнить следующие шаги:
- Захватить первую фотографию (верхний левый элемент).
- Перетащить её в область корзины (Trash).
- Проверить, что после перемещения:
    - В корзине появилась одна фотография.
    - В основной области осталось 3 фотографии.

Ожидаемый результат:
- Фотография успешно перемещается в корзину.
- Вне корзины остаются 3 фотографии.
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


@pytest.fixture
def driver():
    driver = webdriver.Firefox()
    driver.maximize_window()
    yield driver
    driver.quit()


# Задание 1: Проверка текста в iframe
def test_iframe_text(driver):
    driver.get("https://bonigarcia.dev/selenium-webdriver-java/iframes.html")
    wait = WebDriverWait(driver, 10)

    iframe = wait.until(EC.presence_of_element_located((By.ID, "my-iframe")))
    driver.switch_to.frame(iframe)

    elements = driver.find_elements(By.XPATH, "//*")
    target_text = "semper posuere integer et senectus justo curabitur."
    found = False
    for el in elements:
        if el.text and target_text in el.text:
            found = True
            break

    assert found, f"Текст '{target_text}' не найден в iframe"


# Задание 2: Drag & Drop (Перетаскивание фотографии в корзину)
def test_drag_and_drop(driver):
    driver.get("https://www.globalsqa.com/demo-site/draganddrop/")
    wait = WebDriverWait(driver, 15)

    # Решения проблемы с печеньками
    try:
        consent_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//p[text()='Einwilligen']")))
        driver.execute_script("arguments[0].scrollIntoView(true);", consent_button)
        consent_button.click()
    except:
        pass

    demo_iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe.demo-frame")))
    driver.switch_to.frame(demo_iframe)

    images = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#gallery li")))
    trash = wait.until(EC.presence_of_element_located((By.ID, "trash")))

    # Перетаскиваем первую фотографию в корзину
    action = ActionChains(driver)
    action.drag_and_drop(images[0], trash).perform()

    trash_photos = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#trash ul.gallery li"))
    )
    gallery_photos = driver.find_elements(By.CSS_SELECTOR, "#gallery li")

    print(f"\nВ корзине фото: {len(trash_photos)}")
    print(f"В галерее фото: {len(gallery_photos)}")

    # Проверяем количество фото
    assert len(trash_photos) == 1, "Фото не появилось в корзине"
    assert len(gallery_photos) == 3, "Неверное количество фото в галерее"

    driver.switch_to.default_content()