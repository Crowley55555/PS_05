import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Firefox()

url = "https://tomsk.hh.ru/vacancies/programmist"
driver.get(url)

time.sleep(3)

vacancies = driver.find_elements(By.CLASS_NAME, "vacancy-info--ieHKDTkezpEj0Gsx")

parsed_data = []

for vacancy in vacancies:
    try:
        title = vacancy.find_element(By.CSS_SELECTOR, "[data-qa='serp-item__title-text']").text
        company = vacancy.find_element(By.CSS_SELECTOR, "[data-qa='vacancy-serp__vacancy-employer-text']").text

        try:
            salary = vacancy.find_element(By.CSS_SELECTOR, "span.magritte-text_typography-label-1-regular___pi3R-_3-0-32").text.replace('\u00A0', ' ').replace('\u202F', ' ')
        except:
            salary = "Не указана"



        link = vacancy.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

        parsed_data.append([title, company, salary, link])
    except Exception as e:
        print(f"Ошибка при парсинге вакансии: {e}")
        continue

driver.quit()

with open("hh.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Название вакансии", "Название компании", "Зарплата", "Ссылка"])
    writer.writerows(parsed_data)
print(f"Спарсено {len(parsed_data)} вакансий. Данные сохранены в hh.csv")