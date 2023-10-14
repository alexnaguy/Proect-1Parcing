from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from abc import ABC, abstractmethod
import time

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import datetime
import random
from fake_useragent import UserAgent


class FormManage:

    def auto(request):
        """
        Здесь пользователь вводит определенные параметры для выбора автомобиля:
        марка, модель, цена от и до, год выпуска от и до и город для поиска.
        """
        return render(request, 'my_form.html')

    def get_info(request):
        """
        Этот метод возвращает определенные, параметры представленные ниже.
        """

        brand = request.POST.get("brand")
        model = request.POST.get("model")
        price_one = request.POST.get("price_one")
        price_two = request.POST.get("price_two")
        year_one = request.POST.get("year_one")
        year_two = request.POST.get("year_two")
        city = request.POST.get("city")

        return render(request, 'get.html', {"brand": brand,
                                            "model": model,
                                            "price_one": price_one,
                                            "price_two": price_two,
                                            "year_one": year_one,
                                            "year_two": year_two,
                                            "city": city

                                            })

    """
    !!! Не знаю как передать эти параметры brand,
     model,price_one, price_two,year_one, year_two, city
     в класс FilterAvitoCar - в методы: search_button_input,
     change_city_search, input_price_from_filter и т.д. !!!
    """


class WebdriverAbstract(ABC):
    # Абстрактный - потому что можно определить другой
    # браузер и вебдрайвер соответственно
    @abstractmethod
    def connect_proxy(self):
        """
        Подключает различные IPI адреса (прокси серверы)
        """
        pass

    @abstractmethod
    def connect_options_webdriver(self):
        """
        Подключает вебдрайвер и добавляет опции различных IPI адрессов
        """
        pass

    @abstractmethod
    def include_browser(self):
        """
        Подключили вэбдрайвер и применили опции
        """
        pass

    @abstractmethod
    def get_url(self):
        pass


class WebdriverChrome(WebdriverAbstract):
    # Прописать параметры класса- self.options , self.browser
    user_agent: UserAgent()
    options: webdriver.ChromeOptions()
    browser: webdriver.Chrome()

    def __init__(self, url: str):
        self.url = url

    def connect_proxy(self):
        """
        Подключает различные IPI адресса (прокси серверы)
        """
        self.user_agent = UserAgent()

    # ERROR: это точно абстрактный класс?

    def connect_options_webdriver(self):
        """
        Подключает вебдрайвер и добавляет опции различных IPI адрессов
        """
        # Запуск браузера Chrome
        self.options = webdriver.ChromeOptions()
        # Добавил опции для вэбдрайвера
        self.browser = self.options.add_argument(f"user-agent= {self.user_agent.chrome}")

    def include_browser(self):
        """
        Подключили вэбдрайвер и применили опции
        """
        self.browser = webdriver.Chrome(options=self.options)

    def get_url(self):
        """
        Браузер переходит на URL, который передает пользователь
        :return:
        """
        self.browser = self.browser.get(self.url)

    """
    Вот здесь я бы сделал отдельный класс WebdriverChrome, представленный в комментариях выше,
    который потом бы потом наследовали классы FilterAvitoCar и AvitoParse
    Как вы считаете? 
    Чтобы сократить одинаковый код

    ОК

    """


class AbstractClassFilter(ABC):

    # ERROR: не может быть конструктора у абстрактного класса

    @abstractmethod
    def search_button_input(self):
        pass

    @abstractmethod
    def change_city_search(self):
        pass

    @abstractmethod
    def input_price_from_filter(self):
        pass

    @abstractmethod
    def input_price_to_filter(self):
        pass

    @abstractmethod
    def input_year_release_from_filter(self):
        pass

    @abstractmethod
    def input_year_release_to_filter(self):
        pass

    @abstractmethod
    def change_number_owners(self):
        pass

    @abstractmethod
    def change_private_ads(self):
        pass

    @abstractmethod
    def search_button_show_ads(self):
        pass


class FilterAvitoCar(WebdriverChrome, AbstractClassFilter, FormManage):

    def activate_browser(self):
        self.connect_proxy()
        self.connect_options_webdriver()
        self.include_browser()
        self.get_url()
        print("Браузер успешно подключен!")

    def search_button_input(self):
        """
        Находит главную кнопку поиска на сайте Авито,куда затем передаются параметры поиска.
        :return:
        """
        # Нашли кнопку ввода марки и модели автомобиля
        input = self.browser.find_element(By.CSS_SELECTOR, "[data-marker='search-form/suggest']")
        # Ввели в поисковик марку и модель автомобиля (Renault Logan)
        input.send_keys("Renault Logan")
        input.send_keys(Keys.ENTER)
        sleep(3)
        print("Успешно введена модель авто!")

    def change_city_search(self):
        """
        Находит кнопку "Изменить город". Меняет город, на указанный пользователем и
        делает поиск по Объявлениям.
        :return:
        """
        # Нашли кнопку "Поменять город"
        input = self.browser.find_element(By.CSS_SELECTOR, "[class='desktop-nev1ty']").click()
        sleep(2)
        # Нашли кнопку для ввода своего города
        button_city_inp = self.browser.find_element(By.CSS_SELECTOR, "[data-marker='popup-location/region/input']")
        button_city_inp.send_keys(Keys.CONTROL, "a")

        # Нужно передать город, из класса FormManage
        button_city_inp.send_keys('Ярославль')
        sleep(2)
        # Нашли кнопку "Показать обьявления"
        sear = self.browser.find_element(By.CSS_SELECTOR, "[data-marker='popup-location/save-button']").click()
        sleep(1)
        # Дублирую кнопку "Показать обьявления"
        sear = self.browser.find_element(By.CSS_SELECTOR, "[data-marker='popup-location/save-button']").click()
        sleep(5)

    def input_price_from_filter(self):
        """
        Находит кнопку ввода "Цена от" и вводит, указанное пользователем значение цены.
        :return:
        """
        # Нашли кнопку "Цена от"
        inp = self.browser.find_element(By.CSS_SELECTOR, "[data-marker='price/from']")
        # Ожидание
        wait = WebDriverWait(self.browser, timeout=2)
        # Нашли кнопку "Цена от" еще раз
        inp = self.browser.find_element(By.CSS_SELECTOR, "[data-marker='price/from']").click()
        # Ждем пока кнопка не станет доступной для нажатия
        wait.until(lambda d: inp.is_displayed())
        inp.send_keys('500000')
        inp.send_keys(Keys.ENTER)

    def input_price_to_filter(self):
        """
        Находит кнопку ввода "Цена до" и вводит свое значение цены.
        :return:
        """
        inp = self.browser.find_element(By.CSS_SELECTOR, "[data-marker='price/to']")
        inp.send_keys('700000')
        inp.send_keys(Keys.ENTER)
        print("Успешно введены цены !")
        sleep(2)

    def input_year_release_from_filter(self):
        """
        Находит кнопку ввода "Год выпуска от" и вводит свое значение года.

        :return:
        """
        inp = self.browser.find_element(By.CSS_SELECTOR, "[data-marker='params[188]/from/input']")
        inp.send_keys('2005')
        inp.send_keys(Keys.ENTER)

    def input_year_release_to_filter(self):
        """
        Находит кнопку ввода "Год выпуска оо" и вводит свое значение года.

        :return:
        """
        inp = self.browser.find_element(By.CSS_SELECTOR, "[data-marker='params[188]/to/input']")
        inp.send_keys('2010')
        inp.send_keys(Keys.ENTER)
        sleep(3)
        print("Успешно введены года !")

    def change_number_owners(self):
        """
        Выбирает число владельцев автомобиля "Не более двух".
        :return:
        """
        inp = self.browser.find_element(By.CSS_SELECTOR, "[data-marker='option(19984)']")
        inp.click()
        sleep(3)
        print("Успешно выбрано число  владельцев!")

    def change_private_ads(self):
        inp = self.browser.find_element(By.XPATH,
                                        "//*[@id='app']/div/div[4]/div/div[2]/div[3]/div[1]/div/div[2]/div[1]/form/div[30]/div/div/div/div/div/div/div/div[2]/label/span")
        inp.click()
        sleep(3)
        print("Частные объвления выбраны")

    def search_button_show_ads(self):
        inp = self.browser.find_element(By.CSS_SELECTOR, "[data-marker='search-filters/submit-button']")
        inp.click()
        sleep(15)
        print("Идет поиск объявлений по заданным параметрам")

    def activate_func_filter(self):
        self.search_button_input()
        self.change_city_search()
        self.input_price_from_filter()
        self.input_price_to_filter()
        self.input_year_release_from_filter()
        self.input_year_release_to_filter()
        self.change_number_owners()
        self.change_private_ads()
        self.search_button_show_ads()


class AvitoParse(WebdriverChrome):
    # Конструктор класса
    # TODO: у родителя есть конструктор, который нужно переопределить

    def __init__(self, count=100):
        # self.url = url
        self.count = count  # количество страниц на Авито для парсинга
        self.data = []

    def __paginator(self):
        # Находим в браузере кнопку "Следующая страница"
        while self.browser.find_elements(By.CSS_SELECTOR, "[data-marker='pagination-button/next']") and self.count > 0:
            self.__parse_page()
            # Если есть делаем клик на кнопку Next
            self.browser.find_element(By.CSS_SELECTOR, "[data-marker='pagination-button/next']").click()
            self.count -= 1

    # Парсинг одной страницы
    def __parse_page(self):
        """
        Берет все объвления на одной странице и парсит (собирает данные) для каждого значения:
        name, description, url, price, date_car.
        Затем собирает их в список и сохраняет в формате json.
        :return:
        """

        # Находим все объявления
        titles = self.browser.find_elements(By.CSS_SELECTOR, "[data-marker='item']")

        for title in titles:

            # Находим название объявления
            name = title.find_element(By.CSS_SELECTOR, "[itemprop='name']").text

            # description = title.find_element(By.CSS_SELECTOR, "[class*= 'item-descriptionStep']").text
            description = title.find_element(By.CSS_SELECTOR, "[data-marker='item-specific-params']").text
            url = title.find_element(By.CSS_SELECTOR, "[data-marker= 'item-title']").get_attribute("href")
            price = title.find_element(By.CSS_SELECTOR, "[itemprop='price']").get_attribute("content")
            price = price + " " + "руб."
            date_car_par = title.find_element(By.CSS_SELECTOR, "[data-marker='item-date/tooltip/reference']").text
            # date_car = str(date_car_par)[8:10]
            # date_car = int(date_car)
            # Дата сегодня минус день назад
            past_date = str(datetime.datetime.today() - datetime.timedelta(days=1))
            # past_date = int(past_date[8:10])

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
            # print(name, url, price )
        self.save_data()

    def parse(self):
        self.__paginator()
        self.__parse_page()

    def save_data(self):
        """
        Сохраняет записанные данные в формате json.
        :return:
        """
        with open("cars.json", "w", encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
        print(f"Запись произведена успешно.")


if __name__ == "__main__":
    filter_one = FilterAvitoCar(url='https://www.avito.ru/')
    # Должен активировать все методы класса FilterAvitoCar:
    filter_one.activate_browser()
    filter_one.search_button_input()













































