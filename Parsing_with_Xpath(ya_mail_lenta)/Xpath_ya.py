from lxml import html
import requests
from pprint import pprint
import datetime
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['news_parser_db']
collection_ya = db.yandex

def get_yandex_news():
    main_link_ya = 'https://yandex.ru'
    news = '/news/'
    result_ya = []

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

    response = requests.get(main_link_ya + news, headers = headers)
    root = html.fromstring(response.text)
    news_heads_ya = root.xpath("//h2[contains(@class, 'story__title')]/a/text()")
    news_link_ya = root.xpath("//h2[contains(@class, 'story__title')]/a/@href")
    news_date_ya = root.xpath("//div[contains(@class, 'story__date')]/text()")

    #собираем все заголовки
    for item in news_heads_ya:
        dict = {}
        dict['heads'] = news_heads_ya
    result_ya.append(dict)

    #теперь переделываем ссылки:
    main_links=[]
    for i in range(len(news_link_ya)):
        links=main_link_ya + news_link_ya[i]
        main_links.append(links)

    for item in main_links:
        dict={}
        dict['link'] = main_links
    result_ya.append(dict)

    news_date_ya = root.xpath("//div[contains(@class, 'story__date')]/text()")

    source_news=[]
    date_source=[]
    for i in range(len(news_date_ya)):
        data_buf = news_date_ya[i].replace('\xa0',' ').split(' ')
        source_buf = news_date_ya[i].split(' ')
        source_news.append(source_buf)
        date_source.append(data_buf)

    date_ya = []
    for i in range(len(date_source)):
        if "вчера" in date_source[i]:
            date_source[i][-1] = str(datetime.date.today() - datetime.timedelta(1))
            date_ya.append(date_source[i][-1])
        else:
            date_source[i][-1] = datetime.datetime.today().strftime("%Y-%m-%d")
            date_ya.append(date_source[i][-1])

    for item in date_ya:
        dict = {}
        dict['date'] = date_ya
    result_ya.append(dict)

    #отсекаем от списка доты. Оставляем только источники.
    source = []
    for i in range(len(source_news)):
        source_item = source_news[i][:-1]
        source.append((source_item))

    #Снова склеиваем источник через join.
    ya_source=[]
    for i in range(len(source)):
        full_source = ' '.join(source[i])
        ya_source.append(full_source)

    #записываем в общий словарь:
    for item in ya_source:
        dict = {}
        dict['source'] = ya_source
    result_ya.append(dict)

    for dict in result_ya:
        if dict:
            collection_ya.insert_one(dict)

    return (result_ya)


pprint(get_yandex_news())