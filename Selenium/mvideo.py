from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pymongo import MongoClient
import time
import json

client = MongoClient('localhost', 27017)
db = client['mvideo']
collection_hits = db.mvideo

driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://www.mvideo.ru/')
assert 'М.Видео ' in driver.title

driver.execute_script("window.scrollTo(0, 2000)")

hits = WebDriverWait(driver,15).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'sel-hits-block')))[1]

data = []
while True:
    products = WebDriverWait(hits, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'sel-product-tile-title')))

    for product in products:
        df={}
        description = json.loads(product.get_attribute('data-product-info'))
        df['product'] = description['productName']
        df['price'] = description['productPriceLocal']
        df['type_product'] = description['productCategoryName']
        df['producer']=description['productVendorName']
        data.append(df)

    time.sleep(3)

    button = hits.find_element_by_xpath(".//a[contains(@class, 'sel-hits-button-next')]")

    time.sleep(3)

    if 'disabled' in button.get_attribute('class'):
        break
    else:
        button.click()

for dict in data:
    if dict:
        collection_hits.insert_one(dict)
