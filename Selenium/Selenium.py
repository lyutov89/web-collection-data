# 1) Написать программу, которая собирает входящие письма из своего или тестового почтового
# ящика и сложить данные о письмах в базу данных (от кого, дата отправки, тема письма, текст
# письма полный)
# Логин тестового ящика: study.ai_172@mail.ru
# Пароль тестового ящика: NewPassword172
# 2) Написать программу, которая собирает «Хиты продаж» с сайта техники mvideo и складывает
# данные в БД. Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые
# товары

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pymongo import MongoClient
import time

client = MongoClient('localhost', 27017)
db = client['selenium_mail_inbox']
collection_mail = db.mail_inbox

driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://mail.ru/')
assert 'Mail.ru' in driver.title

elem_in = driver.find_element_by_id("mailbox:login")
elem_in.send_keys('study.ai_172@mail.ru')

elem_button = driver.find_element_by_id('mailbox:submit').click()
elem_password = driver.find_element_by_id("mailbox:password")
elem_password.send_keys('NewPassword172')
elem_button = driver.find_element_by_id('mailbox:submit').click()


letter = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.XPATH,"//a[@class='llc js-tooltip-direction_letter-bottom js-letter-list-item llc_pony-mode llc_normal']")))

link = letter.get_attribute('href')
driver.get(link)

assert 'Почта Mail.ru' in driver.title

time.sleep(7)
data = []

while True:
    time.sleep(1)
    df = {}
    df['author'] = driver.find_element_by_class_name('letter-contact').text
    df['topic'] = driver.find_element_by_class_name('thread__subject-line').text
    df['date'] = driver.find_element_by_class_name('letter__date').text
    df['full_text'] = driver.find_element_by_class_name('letter-body').text
    data.append(df)

    time.sleep(2)
    next_page = driver.find_element_by_xpath(
        "//span[@class='button2 button2_has-ico button2_arrow-down button2_pure button2_short button2_compact button2_ico-text-top button2_hover-support js-shortcut']")

    if 'button2_disabled' in next_page.get_attribute('class'):
        break
    else:
        next_page.click()

for dict in data:
    if dict:
        collection_mail.insert_one(dict)



