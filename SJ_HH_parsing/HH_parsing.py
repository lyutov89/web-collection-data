#1) Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы) с сайта
# superjob.ru и hh.ru. Приложение должно анализировать несколько страниц сайта(также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум:

#*Наименование вакансии
#*Предлагаемую зарплату (отдельно мин. отдельно макс. и отдельно валюту)
#*Ссылку на саму вакансию
#*Сайт откуда собрана вакансия
#По своему желанию можно добавить еще работодателя и расположение. Данная структура должна быть одинаковая для вакансий
# с обоих сайтов. Общий результат можно вывести с помощью dataFrame через pandas.

from pprint import pprint
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import numpy as np

main_link_HH = 'https://hh.ru/search/vacancy'
#https://hh.ru/search/vacancy?searchVacancy&text=data+analyst (keywords = data analyst) регион - Россия

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

keywords_hh = input('Введите вакансию для поиска: ')
page_hh_init = int(input('Введите кол-во страниц для анализа: '))
page_n = 0
params_hh = {'text': keywords_hh, 'page': page_n}

response = requests.get(f'{main_link_HH}', headers=headers, params = params_hh).text
soup = bs(response, "lxml")

HH_data=[]

for p in range(0, page_hh_init):
    if soup.find_all('div', {'data-qa': "pager-block"})[0].findChildren()[-2].text == 'дальше':
        page_n += 1

        response = requests.get(f'{main_link_HH}', headers=headers, params=params_hh).text
        soup = bs(response, "lxml")
        HH_block = soup.find_all('div', {'class':'vacancy-serp'})
        HH_list = HH_block[0].find_all('div', {'class': 'vacancy-serp-item' }) + \
                    HH_block[0].find_all('div', {'class': 'vacancy-serp-item  vacancy-serp-item_premium'})

        for HH_vac_list in HH_list:

            HH_main={}

            HH_main['name'] = HH_vac_list.select_one('a.bloko-link.HH-LinkModifier').text
            HH_main['link'] = HH_vac_list.select_one('a.bloko-link.HH-LinkModifier')['href']
            HH_main['employer'] = HH_vac_list.select_one('a.bloko-link.bloko-link_secondary').text
            HH_main['resp'] = HH_vac_list.select_one('div.g-user-content').text

            HH_sal = HH_vac_list.select_one('div.vacancy-serp-item__sidebar').text
            #создадим массив из строчки. Делаем split (разбивку) каждого элемента, удаляем неразрывный пробел.
            salary = HH_sal.replace('\xa0', '').replace('-', ' - ').split(' ')
            #методом pop возвращаем удаленный последний элемент из полученного списка.
            HH_main['currency'] = salary.pop()
            if 'от' in salary:
                HH_main['sal_min'] = int(salary[1])
                HH_main['sal_max'] = np.nan
            elif 'до' in salary:
                HH_main['sal_max'] = int(salary[1])
                HH_main['sal_min'] = np.nan
            elif '-' in salary:
                HH_main['sal_min'] = int(salary[0])
                HH_main['sal_max'] = int(salary[2])
            elif '' in salary:
                HH_main['sal_min'] = np.nan
                HH_main['sal_max'] = np.nan
            else:
                HH_main['sal_min'] = np.nan
                HH_main['sal_max'] = np.nan
                HH_main['currency'] = np.nan

            HH_data.append(HH_main)
    else:
        print(f"Число страниц по запросу: '{page_n + 1}'.")


df = pd.DataFrame(HH_data)
pprint(pd.DataFrame(HH_data))

df.to_csv('HH_data', encoding = 'utf-8')
#Для проверки самих себя выведем кол-во записей. Должно совпасть с кол-вом страниц*50
pprint(len(HH_data))

#Пока мне сложно уложить это в функции, запустить 'if __name__ = 'main' и так далее. Я думаю, это будет моим техническим долгом. Отметил и записал себе.
