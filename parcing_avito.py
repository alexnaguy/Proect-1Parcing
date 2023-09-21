import json

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import datetime

from selenium.webdriver.common.by import By

# driver = uc.Chrome()
# # Заустили сайт авито Бесплатно+Электроника через Chrome
# driver.get("https://www.avito.ru/all/tovary_dlya_kompyutera?q=бесплатно+электроника")

# browser = Chrome()
# url = 'https://www.google.ru/'
# browser.get(url)

class AvitoParse:
#Конструктор класса
    def __init__(self, url: str, items: list= None, count:int = 100, version_main = None ):
        self.url = url
        self.items = items
        self.count = count
        self.version_main = version_main
        self.data = []



#Запуск браузера
    def __set_up(self):
        #self.driver = uc.Chrome(version_main = self.version_main)
        self.driver = Chrome()

#Браузер переходит на URL,который передает пользователь
    def __get_url(self):
        self.driver.get(self.url)

    def __paginator(self):
        #Находим в браузере кнопку "Следующая страница"
        while self.driver.find_elements(By.CSS_SELECTOR, "[data-marker='pagination-button/next']") and self.count > 0:
            self.__parse_page()
            #Если есть делаем клик на кнопку Next
            self.driver.find_element(By.CSS_SELECTOR, "[data-marker='pagination-button/next']").click()
            self.count -= 1



#Парсинг одной страницы
    def __parse_page(self):

        #Находим все объявления
        titles = self.driver.find_elements(By.CSS_SELECTOR,"[data-marker='item']")

        for title in titles:

            #Находим название объявления
            name = title.find_element(By.CSS_SELECTOR, "[itemprop='name']").text

            #description = title.find_element(By.CSS_SELECTOR, "[class*= 'item-descriptionStep']").text
            description = title.find_element(By.CSS_SELECTOR, "[data-marker='item-specific-params']").text
            url = title.find_element(By.CSS_SELECTOR, "[data-marker= 'item-title']").get_attribute("href")
            price = title.find_element(By.CSS_SELECTOR, "[itemprop='price']").get_attribute("content")
            price = price +" " + "руб."
            date_car_par = title.find_element(By.CSS_SELECTOR, "[data-marker='item-date/tooltip/reference']").text
            # date_car = str(date_car_par)[8:10]
            # date_car = int(date_car)
            # Дата сегодня минус день назад
            past_date = str(datetime.datetime.today() - datetime.timedelta(days=1))
            #past_date = int(past_date[8:10])

            # Использвать срез
            if date_car_par > past_date:
                print(date_car_par)
                data = {
                    "name": name,
                    "url": url,
                    "price": price,
                    "description": description,
                    "date": date_car_par

                }

                self.data.append(data)
            else:
                print(f"Объявлений за сегодня не найдено.")
            #print(name, url, price )
        self.save_data()




    def parse(self):
        self.__set_up()
        self.__get_url()
        self.__paginator()
        self.__parse_page()

    def save_data(self):
        with open("cars.json", "w", encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent= 4)
        print(f"Запись произведена успешно.")






if __name__ == "__main__":

    AvitoParse(url= "https://www.avito.ru/all/avtomobili/ford/focus/i-ASgBAgICA0Tgtg2cmCjitg3CpSjqtg3c8ig?cd=1",
                           count = 1,
                           version_main =None,
                           items = None
                            ).parse()






