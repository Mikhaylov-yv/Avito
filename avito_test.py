import requests
from bs4 import BeautifulSoup
# import ast
# import re
# from datetime import datetime, timedelta
#
#
# url = 'https://www.avito.ru/sankt-peterburg/kvartiry/sdam/na_dlitelnyy_srok/studii?p=1'
# r=requests.get(url)
# print(r)
#
# soup = BeautifulSoup(r.text,'lxml')
# pages = soup.find('div',class_='pagination-pages clearfix').find_all('a',class_='pagination-page')[-1].get('href')
# print(pages)
# print(type(pages))
# total_pages = pages.split('=')[1]
# print(total_pages)
# print(type(total_pages))
# abs = soup.find('div', class_ = 'catalog-list js-catalog-list clearfix').find_all('div',class_ ='item_table-wrapper')
# print(len(abs))
# ad = abs[0]
# title = 'https://www.avito.ru/' + ad.find('div', class_='item_table-header').find('h3').find('a').get('href')
# price = ad.find('span', class_='price price_highlight').text
#
# now = datetime.today()
# now_day = now.strftime("%d.%m.%Y")
# yesterday_day = datetime.today() - timedelta(days=1)
# yesterday_day=yesterday_day.strftime("%d.%m.%Y")
#
# def data_preob(item_date):
#     list_data = item_date.split()
#     if list_data[0]=='сегодня':
#         list_data = ' '.join([now_day,list_data[1]])
#     elif list_data[0]=='вчера':
#         list_data = ' '.join([yesterday_day, list_data[1]])
#     else: list_data = ' '.join(list_data)
#     return (list_data)
#
#
#
# item_date = ad.find('div', class_='js-item-date c-2')['data-absolute-date'].strip().lower()
# item_date='вчера 20:08'
#
# print(item_date)
# print(data_preob(item_date))
# print(type(''))

# import csv
# def open_csv(fil_name):
#     links=[]
#     with open('avito.csv', newline='', encoding="utf-8") as f:
#         reader = csv.reader(f,delimiter=';')
#         for row in reader:
#             links.append(row[3])
#     print(links)
#     return links

# import vk_api
# import random
# from my_data import MyVKData_O
#
# vk_session = vk_api.VkApi(token=MyVKData_O.TOKEN)
# vk = vk_session.get_api()
#
# v = 5.92
# random_id = random.randint(0, 999999)
# vk.messages.send(chat_id = 2,
#                  random_id=random_id,
#                  message='привет')

# a= ['Политехническая 700 м','Лесная 1.7 км','Площадь Мужества 3 км']
# metro_plus= a[0].split(' ')
# print(metro_plus)
# for str in reversed(metro_plus):
#     try:
#         distance = float(str)
#         i = metro_plus.index(str)
#     except:
#         continue
#
# metro = ' '.join(metro_plus[:i])
# if metro_plus[i+1] == 'м':
#     metro_plus[i] = float(metro_plus[i])/1000
#     metro_plus[i + 1] = 'км'
# distance = metro_plus[i]
# print(metro, distance)

import vk_api
from my_data import MyVKData_O
v = 5.92
# vk_session = vk_api.VkApi(token=MyVKData_O.TOKEN)
vk_session_wall = vk_api.VkApi(login=MyVKData_O.LOGIN, password=MyVKData_O.GET_PASSWORD)
vk_session_wall.auth()
vk_wall = vk_session_wall.get_api()
print(vk_wall.wall.post(owner_id='-169108750',message='Hello world!',v=v))



# def get_html(url):
#     r=requests.get(url)
#     return r.text
#
# url_gen = 'https://www.avito.ru/sankt-peterburg/kvartiry/1-k_kvartira_40_m_1625_et._1406956663'
# html=get_html(url_gen)
# soup = BeautifulSoup(html, 'lxml')
# print(soup)
# ads = str(soup.find('div', class_ = 'advanced-params'))
# print(ads)