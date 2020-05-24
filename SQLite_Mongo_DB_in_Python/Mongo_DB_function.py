# 1) Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, записывающую собранные
# вакансии в созданную БД
# 2) Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введенной суммы

from pymongo import MongoClient
from pprint import pprint
import pandas as pd
import numpy as np
import csv

df = pd.read_csv('C:/Users/Anatoly/Desktop/Web_parsing/Beautiful_soup/HH_data', sep=',')
df_SJ = pd.read_csv('C:/Users/Anatoly/Desktop/Web_parsing/Beautiful_soup/SJ_data', sep=',')

client = MongoClient('localhost', 27017)

db = client['hh_vac_db']
collection_HH = db.HH_data
collection_SJ = db.SH_data

list_hh = df.to_dict('records')
list_sj = df_SJ.to_dict('records')

collection_HH.insert_many(list_hh)
collection_SJ.insert_many(list_sj)

for col in collection_SJ.find({}):
    pprint(col)

for col in collection_HH.find({}):
    pprint(col)

required_salary = int(input('Введите данные по зарплате '))
result = collection_HH.find({'sal_min':{'$gt' : required_salary}}).sort('sal_min', -1)

result_df = pd.DataFrame.from_dict(result)

print(result_df)
