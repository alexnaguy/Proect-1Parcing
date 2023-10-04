from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import random
from fake_useragent import UserAgent

from abc import ABC, abstractmethod
import time


class AbstractClassFilter(ABC):
    @abstractmethod
    def __init__(self, url: str):
        pass

    @abstractmethod
    def connect_proxy(self):

        """
        Подключает различные IPI адресса (прокси серверы)
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
    def __get_url(self):
        pass

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





class FilterAvitoCar(AbstractClassFilter):

    #Прописать параметры класса- self.options , self.browser
    user_agent: UserAgent()
    options : webdriver.ChromeOptions()
    browser : webdriver.Chrome()


    def __init__(self, url: str):
        self.url = url


    def connect_proxy(self):
        """
        Подключает различные IPI адресса (прокси серверы)
        """
        self.user_agent = UserAgent()

    @abstractmethod
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

    def __get_url(self):
        """
        Браузер переходит на URL,который передает пользователь
        :return:
        """
        self.browser = self.browser.get(self.url)

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

    def change_city_search(self):
        """
        Находит кнопку "Изменить город". Меняет город, на указанный пользователем и
        делает поиск по Объявлениям.
        :return:
        """
        #Нашли кнопку "Поменять город"
        input = self.browser.find_element(By.CSS_SELECTOR, "[class='desktop-nev1ty']").click()
        sleep(2)
        # Нашли кнопку для ввода своего города
        button_city_inp = self.browser.find_element(By.CSS_SELECTOR, "[data-marker='popup-location/region/input']")
        button_city_inp.send_keys(Keys.CONTROL, "a")
        button_city_inp.send_keys('Ярославль')
        sleep(2)
        # Нашли кнопку "Показать обьявления"
        sear = self.browser.find_element(By.CSS_SELECTOR, "[data-marker='popup-location/save-button']").click()
        sleep(1)
        #Дублирую кнопку "Показать обьявления"
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
        inp = self.browser.find_element(By.XPATH,"//*[@id='app']/div/div[4]/div/div[2]/div[3]/div[1]/div/div[2]/div[1]/form/div[30]/div/div/div/div/div/div/div/div[2]/label/span")
        inp.click()
        sleep(3)
        print("Частные объвления выбраны")

    def search_button_show_ads(self):
        inp = self.browser.find_element(By.CSS_SELECTOR, "[data-marker='search-filters/submit-button']")
        inp.click()
        sleep(15)
        print("Идет поиск объявлений по заданным параметрам")




























class FilterManageAvito(WebdriverChrome):




    def search_city_button(self):
        # Нашли кнопку Город +++
        self.input = self.browser.find_element(By.CSS_SELECTOR, "[class='desktop-nev1ty']").click()
        sleep(2)
        # Нашли кнопку ввода города
        sear = self.browser.find_element(By.CSS_SELECTOR, "[data-marker='popup-location/region/input']")
        sear.send_keys(Keys.CONTROL, "a")
        sear.send_keys('Ярославль')
        sleep(2)
        # Нашли кнопку Показать обьявления
        sear = self.browser.find_element(By.CSS_SELECTOR, "[data-marker='popup-location']").click()
        sleep(2)
        sear.send_keys(Keys.ENTER)
        sleep(3)








