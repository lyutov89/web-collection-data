from pprint import pprint
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import numpy as np

main_link_SJ = 'https://russia.superjob.ru'

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

keywords_sj = input('Введите вакансию для поиска: ')
page_init_sj = int(input('Введите кол-во страниц для анализа '))
page_n = 0
params_sj = {'keywords': keywords_sj, 'page': page_n}

response = requests.get(f'{main_link_SJ}/vacancy/search/', headers=headers, params = params_sj).text
soup = bs(response, "lxml")

SJ_data = []

for p in range(0, page_init_sj):
    if soup.find_all('div', {'class': "L1p51"})[0].findChildren()[-1].text == 'Дальше':
        page_n += 1
        params_sj = {'keywords': keywords_sj, 'page': page_n}
        response = requests.get(f'{main_link_SJ}/vacancy/search/', headers=headers, params=params_sj).text
        soup = bs(response, "lxml")
        SJ_block = soup.find_all('div', {'class':'_1ID8B'})
        SJ_list = SJ_block[0].find_all('div', {'class': '_3zucV f-test-vacancy-item _3j3cA RwN9e _3tNK- _1NStQ _1I1pc'})

        for sj_vac_list in SJ_list:

            SJ_main = {}
            buf_list = sj_vac_list.find_all('div', {'class': '_3mfro CuJz5 PlM3e _2JVkc _3LJqf'})

            if buf_list:
                SJ_main['name_sj'] = buf_list[0].find('a').text
                SJ_main['link_sj'] = main_link_SJ + buf_list[0].select_one('a')['href']
                sal_sj = sj_vac_list.find('span', {'class': '_3mfro _2Wp8I _31tpt f-test-text-company-item-salary PlM3e _2JVkc _2VHxz'}).text

                salary = sal_sj.replace('\xa0', ' ').replace('-', ' - ').split(' ')

                SJ_main['currency'] = np.nan if 'По' in salary else salary[-1]

                if 'от' in salary:
                    SJ_main['sal_min'] = int(salary[1]+salary[2])
                    SJ_main['sal_max'] = np.nan
                elif 'до' in salary:
                    SJ_main['sal_max'] = int(salary[1]+salary[2])
                    SJ_main['sal_min'] = np.nan
                elif '—' in salary:
                    SJ_main['sal_min'] = int(salary[0]+salary[1])
                    SJ_main['sal_max'] = int(salary[3]+salary[4])
                elif 'По' in salary:
                    SJ_main['sal_min'] = np.nan
                    SJ_main['sal_max'] = np.nan
                    SJ_main['currency'] = np.nan
                else:
                    SJ_main['sal_min'] = np.nan
                    SJ_main['sal_max'] = np.nan
                    SJ_main['currency'] = np.nan

            else:
                continue
            SJ_data.append(SJ_main)

df_SJ = pd.DataFrame(SJ_data)

pprint(pd.DataFrame(SJ_data))
df_SJ.to_csv('SJ_data', encoding = 'utf-8')

print(len(SJ_data))
