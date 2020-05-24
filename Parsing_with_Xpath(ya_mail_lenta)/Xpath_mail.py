from lxml import html
import requests
from pprint import pprint
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['news_parser_db']


def get_mail_news():
    collection_mail = db.news
    main_link_mail = 'https://news.mail.ru'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    response = requests.get(main_link_mail, headers = headers)
    root = html.fromstring(response.text)
    result_mail = []

    #первые шесть новостей заголовков:
    news_heads_mail = root.xpath("//span[contains(@class, 'newsitem__title-inner')]/text()")
    for item in news_heads_mail:
        dict={}
        dict['heads']=news_heads_mail
    result_mail.append(dict)

    #ссылки к первой шестерке новостей:
    news_link_mail = root.xpath("//a[contains(@class, 'newsitem__title link-holder')]/@href")

    mail_link=[]
    for i in range(len(news_link_mail)):
        link = main_link_mail + news_link_mail[i]
        mail_link.append(link)

    for item in mail_link:
        dict={}
        dict['link'] = mail_link
    result_mail.append(dict)

    #добавляем источники в словарь:
    news_link_source = root.xpath("//span[contains(@class, 'newsitem__param')][2]/text()")
    for item in news_link_source:
        dict={}
        dict['source']=news_link_source
    result_mail.append(dict)

    #добавляем дату в словарь:
    news_link_time = root.xpath("//span[contains(@class, 'newsitem__param js-ago')]/@datetime")

    mail_time = []
    for i in range(len(news_link_time)):
        time_buf = news_link_time[i].replace('T', ':').split(':')[0]
        mail_time.append(time_buf)

    for item in mail_time:
        dict={}
        dict['time']=mail_time
    result_mail.append(dict)

    for dict in result_mail:
        if dict:
            collection_mail.insert_one(dict)

    return (result_mail)

pprint(get_mail_news())

