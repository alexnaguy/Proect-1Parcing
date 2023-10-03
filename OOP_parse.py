from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import random
from fake_useragent import UserAgent

from abc import ABC, abstractmethod
import time


class WebdriverChrome:

    #Прописать параметры класса- self.options , self.browser
    user_agent: UserAgent()
    options : webdriver.ChromeOptions()
    browser : webdriver.Chrome()


    def __init__(self, url: str):
        self.url = url
        #Браузеры могут быть разные и опции к ним
        #self.webdrivers


    @abstractmethod
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



    # Браузер переходит на URL,который передает пользователь
    def __get_url(self):
        self.browser = self.browser.get(self.url)



class AbstractFilter(WebdriverChrome):


    def search_button(self):
        # by_selector = By.CSS_SELECTOR
        # selector = "[data-marker='search-form/suggest']"
        button = self.browser.find_element(By.CSS_SELECTOR, "[data-marker='search-form/suggest']")














    def input_query(self, query):






class FilterManageAvito(WebdriverChrome):


    def search_input_button(self):
        """
        Находит кнопку ввода для поиска марки и модели
        """
        # !!!! Нужен ли для переменной input- "self" ?

        # Нашли кнопку ввода марки и модели автомобиля
        input = self.browser.find_element(By.CSS_SELECTOR, "[data-marker='search-form/suggest']")
        # Вбили в поисковик Марку модель (Renault Logan)

        input.send_keys("Renault Logan")
        # Нажали ENTER
        input.send_keys(Keys.ENTER)
        sleep(3)

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








