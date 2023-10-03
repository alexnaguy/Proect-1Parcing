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

        # brand = request.POST.get("brand")
        # model = request.POST.get("model")
        # price_one = request.POST.get("price_one")
        # price_two = request.POST.get("price_two")
        # year_one = request.POST.get("year_one")
        # year_two = request.POST.get("year_two")
        # city = request.POST.get("city")

# Список Юзер-агентов (замена IPI адрессов)
# user_agents_list = [
#     "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
#     "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
#     "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
# ]
#Создали класс Юзкр-агентов (список IPI адрессов)
user_agent = UserAgent()

options = webdriver.ChromeOptions()
# Добавили опции
options.add_argument(f"user-agent= {user_agent.chrome}")
# Применили опции
browser = webdriver.Chrome (
    options= options)
#browser.get(url="https://www.whatsmybrowser.org")
#browser = Chrome()

#++++
url = 'https://www.avito.ru/'
browser.get(url)
#Берем данные из VSCOde и переносим сюда
#Нашли кнопку
inp = browser.find_element(By.CSS_SELECTOR,"[data-marker='search-form/suggest']")
# Вбили в поисковик brand + model
search = inp.send_keys('Renault Logan')
#Нажали ENTER
inp.send_keys(Keys.ENTER)
sleep(3)

#Найти кнопку Город +++
inp = browser.find_element(By.CSS_SELECTOR, "[class='desktop-nev1ty']").click()
sleep(2)
#Нашли кнопку ввода
sear = browser.find_element(By.CSS_SELECTOR,"[data-marker='popup-location/region/input']")
sear.send_keys(Keys.CONTROL, "a")
#city
sear.send_keys('Ярославль')

sleep(2)
#Показать обьявления



sear = browser.find_element(By.CSS_SELECTOR, "[data-marker='popup-location/save-button']").click()
sleep(1)
sear = browser.find_element(By.CSS_SELECTOR, "[data-marker='popup-location/save-button']").click()


sleep(5)


#Цена от   до
# price_one = request.POST.get("price_one")
# price_two = request.POST.get("price_two")
inp = browser.find_element(By.CSS_SELECTOR, "[data-marker='price/from']")
wait = WebDriverWait(browser, timeout=2)

browser.find_element(By.CSS_SELECTOR, "[data-marker='price/from']").click()
wait.until(lambda d: inp.is_displayed())

# inp = browser.find_element(By.CSS_SELECTOR,"[data-marker='price/from']")
inp.send_keys('500000')
inp.send_keys(Keys.ENTER)

inp = browser.find_element(By.CSS_SELECTOR,"[data-marker='price/to']")
inp.send_keys('700000')
inp.send_keys(Keys.ENTER)
print("Успешно введены цены !")
sleep(2)

#Год  от .... до
inp = browser.find_element(By.CSS_SELECTOR, "[data-marker='params[188]/from/input']")
inp.send_keys('2005')
inp.send_keys(Keys.ENTER)

inp = browser.find_element(By.CSS_SELECTOR, "[data-marker='params[188]/to/input']")
inp.send_keys('2010')
inp.send_keys(Keys.ENTER)
sleep(3)
print("Успешно введены года !")
#Число владельцев по ПТС
print(f"________________________мы тут")
inp = browser.find_element(By.CSS_SELECTOR, "[data-marker='option(19984)']")
inp.click()
sleep(3)
print("Успешно выбрано число  владельцев!")
# Частные объявления
inp = browser.find_element(By.XPATH, "//*[@id='app']/div/div[4]/div/div[2]/div[3]/div[1]/div/div[2]/div[1]/form/div[30]/div/div/div/div/div/div/div/div[2]/label/span")
inp.click()
sleep(3)
print("Частные объвления")

inp = browser.find_element(By.CSS_SELECTOR, "[data-marker='search-filters/submit-button']")
inp.click()
sleep(15)
print("Все успешно")





























