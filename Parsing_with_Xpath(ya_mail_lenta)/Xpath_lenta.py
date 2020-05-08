from lxml import html
import requests
from pprint import pprint
import datetime
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['news_parser_db']
collection_lenta = db.lenta

#Для ленты придется организовать словарь, чтобы привести данные к единообразцию:

months = {
'января': '01',
'февраля': '02',
'марта': '03',
'апреля': '04',
'мая': '05',
'июня': '06',
'июля': '07',
'августа': '08',
'сентября': '09',
'октября': '10',
'ноября': '11',
'декабря': '12',
}

def get_lenta_news():
    main_link_lenta = 'https://lenta.ru'

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

    response = requests.get(main_link_lenta, headers = headers)
    root = html.fromstring(response.text)
    result_lenta = []

    #собираем ссылки:
    news_link_lenta = root.xpath("//div[contains(@class, 'titles')]/h3/a/@href")

    main_links=[]
    for i in range(len(news_link_lenta)):
        if 'https' in news_link_lenta[i]:
            news_link_lenta[i]=news_link_lenta[i]
            main_links.append(news_link_lenta[i])
        else:
            link_lenta=main_link_lenta + news_link_lenta[i]
            main_links.append(link_lenta)

    for item in main_links:
        dict={}
        dict['link']=main_links
    result_lenta.append(dict)

    #собираем заголовки
    news_heads_lenta = root.xpath("//div[contains(@class, 'titles')]/h3/a/span/text()")
    for item in news_heads_lenta:
        dict={}
        dict['heads']=news_heads_lenta
    result_lenta.append(dict)

    #собираем даты
    news_data_lenta = root.xpath("//span[contains(@class, 'g-date item__date')]/text()")

    for i in range(len(news_data_lenta)):
        if news_data_lenta[i] == 'Сегодня':
            news_data_lenta[i] = datetime.datetime.today().strftime("%Y-%m-%d")
        else:
            day = news_data_lenta[i].split(' ')[0]
            month = months[news_data_lenta[i].split(' ')[1]]
            year = str(datetime.datetime.now().year)
            news_data_lenta[i] = year + "-" + month + "-" + day

    for item in news_data_lenta:
        dict={}
        dict['data']=news_data_lenta
    result_lenta.append(dict)

    for dict in result_lenta:
        if dict:
            collection_lenta.insert_one(dict)

    return (result_lenta)

pprint(get_lenta_news())

