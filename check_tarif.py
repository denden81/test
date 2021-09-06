from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.implicitly_wait(30)
driver.maximize_window()
import random
import time

# расскоментировать тариф и период нужный для проверки,дефолтные закоментировать.
# tarif = "century"
#tarif = "year"
tarif = "optimo"
#tarif = "millennium"

#period = "Оплата помесячно"
period = "При оплате за год"


# присваиваем текст для проверки тарифа
if tarif == "century":
    tarifLk = "Century+"
if tarif == "year":
    tarifLk = "Year+"
if tarif == "millennium":
    tarifLk = "Millennium+"
if tarif == "optimo":
    tarifLk = "Optimo+"
if tarif == "year":
    worldBase = "база"
    worldSite = "сайт / ftp акк."
else:
    worldBase = "баз"
    worldSite = "сайтов / ftp акк."
if period == "Оплата помесячно":
    periodprice = "periodprice mb20"
else:
    periodprice = "periodprice"
# генерируем рандомное число для емайл.
randomRnd = random.randint(1, 900000)
driver.get("https://timeweb.com/ru/services/hosting/")
# переключаем выбранный период
driver.find_element_by_xpath(
    "//td[@data-code='" + tarif + "']/div/div/label[contains(text(),'" + period + "')]").click()
# получаем текст с сайта для проверки данных в лк
gb = driver.find_element_by_xpath(
    "//td[@data-code='" + tarif + "']//div[contains(text(),'Gb места')]/./strong[@class='w25 dib']").text
site = driver.find_element_by_xpath(
    "//td[@data-code='" + tarif + "']//div[contains(text(),'" + worldSite + "')]/./strong[@class='w25 dib']").text
base = driver.find_element_by_xpath(
    "//td[@data-code='" + tarif + "']//div[contains(.,'" + worldBase + "')]/./strong[@class='w25 dib']").text
price = driver.find_element_by_xpath(
    "//td[@data-code='" + tarif + "']/div/div[@class='" + periodprice + "']//.//span[@class='price']").text
# вырезаем первые 3 символа в строке абонентской платы,если тариф year то вырезаем 2 символа,если тариф year и период помесячно, то вырезаем 3 символа
if tarif == "year":
    if period == "Оплата помесячно":
        firstSymbolPrice = price[0:3]
    else:
        firstSymbolPrice = price[0:2]
    price = firstSymbolPrice
else:
    secondSymbolPrice = price[0:3]
    price = secondSymbolPrice
# при тарифе милленниум число баз равно бесконечности, присваиваем 0
if tarif == "millennium":
    base = "0"
driver.find_element_by_xpath("//td[@data-code='" + tarif + "']//a[contains(text(),'Разместить сайт')]").click()
# вводим фио и почту
driver.find_element_by_xpath(
    "//div[contains(text(),'Фамилия, имя и отчество*:')]//..//input[@name='full_name']").send_keys("Test user")
driver.find_element_by_xpath("//div[contains(text(),'Электронная почта*:')]//..//input[@name='email']").send_keys(
    str(randomRnd) + "@mailnesia.com")
driver.find_element_by_xpath("//label[contains(text(),'Я согласен с')]").click()
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//a[@class[contains(.,'btn flr')] and contains(.,'Заказать')]")),
    message='Не найдена кнопка Заказать')
driver.find_element_by_xpath("//a[@class[contains(.,'btn flr')] and contains(.,'Заказать')]").click()
# проверяем что есть надпись успешного входа
driver.find_element_by_xpath("//span[contains(.,'Поздравляем!')]")
driver.find_element_by_xpath("//p[contains(.,'Ваш аккаунт готов к работе. Что дальше:')]")
# проверка произодительности отрисовки анимации всплываюшего окна и кнопки закрытия ,за 2 сек должен появится элемент закрытия.
time.sleep(2)
driver.find_element_by_xpath("//button[@type='button']").click()
# проверяем текст  выбранного тарифа
driver.find_element_by_xpath("//h3[contains(text(),'Тариф:')]/a[contains(text(),'" + tarifLk + "')]")
# получаем текст с лк для проверки данных со страницы тарифов хостинга
gbLk = driver.find_element_by_xpath(
    "//h4[contains(text(),'Диск (SSD), ГБ')]//..//span[@class='tariff-info-count-all']").text
siteLk = driver.find_element_by_xpath("//h4[contains(text(),'Сайтов:')]//..//span[@class='tariff-info-count-all']").text
baseLk = driver.find_element_by_xpath(
    "//h4[contains(text(),'Баз данных MySQL:')]//..//span[@class='tariff-info-count-all']").text
priceLk = driver.find_element_by_xpath("//a[contains(text(),'Абонентская плата')]//..//p[@class='cpS-h-XS']").text
# вырезаем первые 3 символа в строке абонентской платы,если тариф year то вырезаем 2 символа
if tarif == "year":
    if period == "Оплата помесячно":
        firstSymbolPriceLk = priceLk[0:3]
    else:
        firstSymbolPriceLk = priceLk[0:2]
    priceLk = firstSymbolPriceLk
else:
    secondSymbolPriceLk = priceLk[0:3]
    priceLk = secondSymbolPriceLk
# вырезаем последние 2 символа в строке количества сайтов,если тариф year то вырезаем 1 символ
lastSymbolSite = siteLk[-1]
if tarif == "year":
    siteLk = (lastSymbolSite)
else:
    preconditionsSymbolSite = siteLk[-2]
    siteLk = (preconditionsSymbolSite + lastSymbolSite)
# вырезаем последние 2 символа в строке количества баз данных,если тариф year то вырезаем 1 символ
lastSymbolBase = baseLk[-1]
if tarif == "year":
    baseLk = (lastSymbolBase)
else:
    preconditionsSymbolBase = siteLk[-2]
    baseLk = (preconditionsSymbolBase + lastSymbolBase)
# при тарифе милленниум число баз равно бесконечности, присваиваем 0
if tarif == "millennium":
    baseLk = "0"
# сравниваем данные с лк и со страницы тарифов хостинга
if price != priceLk:
    print("Абонентская плата в ЛК ", priceLk, " за выбранный период ", period, " не совпадает с заявленным на сайте ",
          price)
else:
    print("Абонентская плата в ЛК ", priceLk, " за выбранный период ", period, " совпадает с заявленным на сайте ",
          price)
if gb != gbLk:
    print("Объем диска(SSD) в ЛК ", gbLk, " не совпадает с заявленным на сайте ", gb)
else:
    print("Объем диска(SSD) в ЛК ", gbLk, " совпадает с заявленным на сайте ", gb)
if siteLk != site:
    print("Количество сайтов в ЛК ", siteLk, " не совпадает с заявленным на сайте ", site)
else:
    print("Количество сайтов в ЛК ", siteLk, " совпадает с заявленным на сайте ", site)
if baseLk != base:
    print("Количество Баз данных MySQL: в ЛК", baseLk, " не совпадает с заявленным на сайте ", base)
else:
    print("Количество Баз данных MySQL: в ЛК", baseLk, " совпадает с заявленным на сайте ", base)
# чекаем ящик ,что письмо о регистрации пришло
driver.get("http://www.mailnesia.com")
driver.find_element_by_id("mailbox").send_keys(str(randomRnd) + "@mailnesia.com")
driver.find_element_by_xpath("//input[contains(@type,'submit')]").click()
driver.find_element_by_xpath("//a[contains(text(),'Timeweb')]//..//..//a[contains(text(),'успешно создан')]")
# чистим ящик от писем чтобы не оставлять следов
driver.find_element_by_xpath("//img[@alt='Delete all mail']").click()
driver.find_element_by_xpath("//input[@value='YES delete them !']").click()
driver.find_element_by_xpath("//div[@id='empty_mailbox']")
driver.close()
