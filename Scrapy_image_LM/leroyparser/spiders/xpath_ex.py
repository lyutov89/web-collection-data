import requests
from lxml import html
import re
import os
from urllib.parse import urlparse

start_urls = 'https://leroymerlin.ru/product/lyustra-favourite-feerie-1932-6p-6-lamp-12-m-90134168/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

response = requests.get(start_urls, headers=headers)

root = html.fromstring(response.text)
price = root.xpath("//uc-pdp-price-view[@class='primary-price']/span[@slot='price']/text()")
number_price = int(price[0].replace(' ', ''))  #61820
name = root.xpath("//uc-pdp-card-ga-enriched[@class='card-data']/h1/text()") #['Светильник встраиваемый R75 GХ53 13 Вт цвет черный хром']

link=response.url #https://leroymerlin.ru/product/lyustra-favourite-feerie-1932-6p-6-lamp-12-m-90134168/

photos = root.xpath("//img[@data-origin]") #https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_1200,h_1200,c_pad,b_white,d_photoiscoming.png/LMCode/90134168_01.jpg
tech_char = root.xpath("//dt[@class = 'def-list__term']/text()")
params_for_tech = root.xpath("//dd[@class = 'def-list__definition']/text()")
link = 'https://leroymerlin.ru/product/lyustra-favourite-feerie-1932-6p-6-lamp-12-m-90134168/'

new_l = link.split('/')[-2].replace('-','_')

#file_name = os.path.basename(urlparse(request.url).path)
#print(file_name)

file_name = '18710617.jpg'
n_file_name = file_name[:8]
print(n_file_name)

file_path = 'C:\\Users\\Anatoly\\PycharmProjects\\LMparser\\leroyparser\\images\\svetilnik_shar_nbb_1he27h60_vt_plastik_81956598'
print(file_path[-8:])
