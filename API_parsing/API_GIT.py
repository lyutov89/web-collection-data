# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
#сохранить JSON-вывод в файле *.json.

# 2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

# User Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36

import requests
import json
from pprint import pprint

buf_user = input('Введите имя юзера, чтобы увидеть его репозитарий ')
git_end_user = 'user:' + buf_user

#использую конкатенацию, чтобы было приятнее вводить имя пользователя. Будьте внимательны. Ошибки от неправильного ввода я не обработал.

main_link = 'https://api.github.com/search/repositories'
headers = {'Accept': 'application/vnd.github.mercy-preview+json'}
params = {'q': git_end_user}
response = requests.get(main_link, headers=headers, params=params)
#response = requests.get('https://api.github.com/search/repositories?q=user:lyutov89')
if response.ok:
    data = json.loads(response.text)
    repositary = []
for i in range(len(data['items'])):
    repositary.append(data['items'][i]['name'])
    #print(data['items'][i]['name'])

print(f'Пользователь {buf_user} создал {data["total_count"]} репозитариев: {", ".join(repositary)}. ')

#записываем данные в формат json.

with open ('repositary_user.json', 'w', encoding='utf-8') as fj:
    json.dump(repositary, fj)

#pprint(data['items'][0]['name'])
#pprint(repositary)


