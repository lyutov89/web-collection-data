#ДЗ №1. Задача №2.
# Изучить список API. Найти среди них любые, требующие авторизацию. Выполнить запрос к нему, пройдя авторизацию. Ответ записать
# в json файл.

# Комментарий: сначала хотел взять Yahoo Finance. Но потом увидел, что нужно привязать карту к их сервису и в случае
# превышения запросов по apikey деньги будут сниматься автоматически. Выбрал сервис twelvedata.com, который предоставляет
# доступ к историческим данным ценных бумаг, рынку форекс и криптовалют. Их apikey можно гонять бесконечно...

import requests
from pprint import pprint
import json

#Access to historical and real-time stocks, forex and cryptocurrencies quotes.

main_link = "https://api.twelvedata.com/time_series"   #каждый запрос еще может заканчиваться technical indicator

apikey = 'df810d92804c4f29a7a0257e742cc510'
interval = '1min' #Interval of output data series (1min, 5min, 15min, 30min, 45min, 1h, 2h, 4h, 1day, 1week, 1month)
stock = 'AAPL:NASDAQ' #бумага и биржа, на которой она торгуется

params = {"symbol":stock,"interval":interval,"apikey": apikey}

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

response = requests.get(main_link, headers=headers, params=params)
if response.ok:
    data = json.loads(response.text)

pprint(response.text)

with open ('AAPL-data.json', 'w', encoding='utf-8') as fj:
    json.dump(data, fj)

#token = df810d92804c4f29a7a0257e742cc510