import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
import time

# Настройки Firefox
options = Options()
options.headless = True
options.set_preference("intl.accept_languages", "ru")

# Инициализация драйвера
driver = webdriver.Firefox(options=options)

# Ссылки на категории
categories = {
    "Диваны": "https://www.divan.ru/category/divany-i-kresla",
    "Кресла": "https://www.divan.ru/category/kresla",
    "Светильники": "https://www.divan.ru/category/svet"
}

def parse_product_card(product):
    try:
        name = product.find_element(By.CSS_SELECTOR, "div.lsooF span").text.strip()
    except NoSuchElementException:
        name = "Нет названия"

    try:
        price = product.find_element(By.CSS_SELECTOR, "div.pY3d2 span").text.strip() + " руб."
    except NoSuchElementException:
        price = "Цена не указана"

    try:
        link = product.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
    except NoSuchElementException:
        link = "Ссылка не найдена"

    return {
        "Категория": current_category,
        "Название": name,
        "Цена": price,
        "Ссылка": link
    }

# Создаем CSV файл
with open("divan_products.csv", mode="w", newline="", encoding="utf-8") as file:
    # Указываем ВСЕ поля, которые будут в словаре
    fieldnames = ["Категория", "Название", "Цена", "Ссылка"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    for category_name, url in categories.items():
        current_category = category_name
        print(f"Парсим категорию: {category_name}")

        driver.get(url)
        time.sleep(3)

        # Прокрутка страницы
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        products = driver.find_elements(By.CSS_SELECTOR, "div.WdR1o")
        print(f"Найдено товаров: {len(products)}")

        for product in products:
            product_data = parse_product_card(product)
            writer.writerow(product_data)
            print(f"Добавлен: {product_data['Название']}")

driver.quit()
print("Парсинг завершен. Данные сохранены в divan_products.csv")