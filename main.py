import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from urllib.parse import quote


def parse_real_estate_agencies(keyword, locations):
    results = []

    for page in range(1, 10):
        '''
        # Инициализация WebDriver
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Запуск в безголовом режиме (без отображения браузера)
        #service = Service(' /Users/deadbadunicorn/Desktop/agent/chromedriver ')  # Укажите путь к chromedriver
        service = Service(' C:/Users/Guslik/Desktop/chrome-win64')

        driver = webdriver.Chrome(service=service, options=chrome_options)'''
        options = Options()
        options.add_argument("--start-maximized")

        service = Service('')
        driver = webdriver.Chrome(service=service, options=options)
        print(driver)

        try:
            for location in locations:
                search_term = f"{keyword} {location}"
                encoded_search_term = quote(search_term)
                search_url = f"https://www.google.com/maps/search/{encoded_search_term}"
                driver.get(search_url)
                time.sleep(2)  # Пауза для загрузки страницы
                # Ожидание появления результатов поиска
                wait = WebDriverWait(driver, 10)
                # element = driver.find_elements(By.CLASS_NAME, "hfpxzc")
                # print(element)
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "hfpxzc")))
                # print("go")
                # Получение списка всех элементов с результатами поиска
                listings = driver.find_elements(By.CLASS_NAME, "hfpxzc")
                listings2 = driver.find_elements(By.CLASS_NAME, "UsdlK")
                listings3 = driver.find_elements(By.CLASS_NAME, "W4Efsd")

                for i in range(len(listings)):
                    title = listings[i].get_attribute("aria-label")
                    website_url = listings[i].get_attribute("href")
                    for j in range(len(listings2)):
                        phone = listings2[j].text
                        for k in range(len(listings3)):
                            address = listings3[j].find_element(By.XPATH, "//div[@class='W4Efsd']//span[2]/span[2]")
                    # adr = address.find_element(By.CSS_SELECTOR, ".W4Efsd > span:nth-child(1)").text
                    # adr = ""
                    # for address in addresses:
                    #     adr += address.text + ","
                            adr = address.text
                    # address = listings3[i].find_element(By.XPATH, "//span[2]/span[2]").text


                print(f"Название: {title}")
                print(f"Телефон: {phone}")
                # print(f"Адрес: {address}")
                print(f"Адрес: {adr}")
                print(f"Ссылка на сайт: {website_url}")

                results.append({
                    "Название": title,
                    "Адрес": adr,
                    "Телефон": phone,
                    "Ссылка на сайт": website_url
                })

        finally:
            driver.quit()  # Закрытие WebDriver после завершения парсинга

    return results


if __name__ == "__main__":
    keyword = "агентство недвижимости"
    locations = ["ОАЭ", "Таиланд", "Турция", "Бали", "Кипр"]

    try:
        print(f"Выполняется парсинг данных для запроса: '{keyword}'...")
        parsed_data = parse_real_estate_agencies(keyword, locations)
        if parsed_data:
            # Сохранение данных в файл Excel
            df = pd.DataFrame(parsed_data)
            df.to_excel('real_estate_agencies.xlsx', index=False)
            print("Данные успешно сохранены в файл 'real_estate_agencies.xlsx'")
        else:
            print("Не удалось найти результаты для запроса")

    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
