import requests
from bs4 import BeautifulSoup
import re
import csv
import time
from datetime import datetime, timedelta
import vk_api
import random
from my_data import MyVKData_O
import config_avito
from proxy import Proxy_next
import logging

now = datetime.today()
now_day = now.strftime("%d.%m.%Y")
yesterday_day = datetime.today() - timedelta(days=1)
yesterday_day=yesterday_day.strftime("%d.%m.%Y")

def open_csv(fil_name):
    links=[]
    with open(fil_name, newline='', encoding="utf-8") as f:
        reader = csv.reader(f,delimiter=';')
        for row in reader:
            links.append(row[4])
    return links

def get_html(url):
    r=requests.get(url)
    return r.text

def get_total_pages(html):
    soup = BeautifulSoup(html,'lxml')
    pages = soup.find('div', class_='pagination-pages clearfix').find_all('a', class_='pagination-page')[-1].get('href')
    total_pages = pages.split('=')[1].split('&')[0]
    return int(total_pages)

def text_clear(text):
    reg = re.compile('[^а-яА-яёЁ1-9 ]')
    text = reg.sub(' ', str(text))
    text = re.sub(" +", " ", text)
    return text

def price_clear(price):
    reg = re.compile('[^0-9]')
    price = reg.sub('', str(price))
    return price

def write_csv(data,fil_name):
    with open(fil_name, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow((data['title'],data['price'],data['metro'],str(data['distance']).replace('.',','),data['url'],data['address'],data['item_date']))

def data_preob(item_date):
    list_data = item_date.split()
    if list_data[0]=='сегодня':
        list_data = ' '.join([now_day,list_data[1]])
    elif list_data[0]=='вчера':
        list_data = ' '.join([yesterday_day, list_data[1]])
    else: list_data = ' '.join(list_data)
    return (list_data)

def distance_metro(metro_plus):
    metro_plus = metro_plus.split(' ')
    for str in reversed(metro_plus):
        try:
            distance = float(str)
            i = metro_plus.index(str)
        except:
            continue
    metro = ' '.join(metro_plus[:i])
    if metro_plus[i + 1] == 'м':
        metro_plus[i] = float(metro_plus[i]) / 1000
        metro_plus[i + 1] = 'км'
    distance = metro_plus[i]
    return (metro, distance)

def get_page_data(html,fil_name,links,vk,vk_wall):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('div', class_ = 'catalog-list js-catalog-list clearfix').find_all('div',class_ ='item_table-wrapper')
    for ad in ads:
        try:
            title = ad.find('div', class_='item_table-header').find('h3').text.strip()
        except:
            title = ''
        try:
            url = 'https://www.avito.ru' + ad.find('div', class_='item_table-header').find('h3').find('a').get('href')
            if url in links: continue
        except:
            url = ''
        try:
            price = price_clear(ad.find('span', class_='price').text)
        except:
            print(ad.find('span', class_='price'))
            price = ''
        try:
            metro_plus = ad.find('p', class_='address').text.split(',')[0].strip()
            metro_plus = distance_metro(metro_plus)
            metro = metro_plus[0]
            distance = metro_plus[1]
        except:
            metro = ''
            distance = ''
        try:
            address = text_clear(str(ad.find('p', class_='address').text.split(',')[1:])).strip()
        except:
            address = ''
        for n in config_avito.list_metro:
            metro_ = False
            if metro.lower().count(n) > 0:
                metro_ = True
                break
        if metro_ == False: continue
        try:
            item_date = data_preob(ad.find('div', class_='js-item-date c-2')['data-absolute-date'].strip().lower())
        except:
            print(ad.find('div', class_='js-item-date c-2'))
            item_date = ''
        messages = str(title + '; ' + metro + ' ' + str(distance) + 'км; ' + price + '; ')
        if float(distance)<config_avito.metr_distance and int(price)<config_avito.max_price:
            messages_send(messages,url, vk)
            wall_post(messages, url, vk_wall)
        data = {'title': title, 'url': url, 'price': price, 'metro': metro,'distance':distance, 'address': address,'item_date':item_date}
        write_csv(data,fil_name)
def get_page_data_post (html):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('div', class_ = 'catalog-list js-catalog-list clearfix').find_all('div',class_ ='item_table-wrapper')

def wall_post(text,url,vk):
    v = 5.92
    time.sleep(5)
    vk.wall.post(owner_id='-169108750',
                 message=text,
                 attachment= url,v=v)

def messages_send(text,url,vk):
    v = 5.92
    random_id = random.randint(0, 999999)
    time.sleep(1/3)
    vk.messages.send(chat_id = 1,
                     random_id=random_id,
                     message = text,
                     attachment= url)


# https://www.avito.ru/sankt-peterburg/kvartiry/sdam/na_dlitelnyy_srok?user=1&f=550_5702-5703-5704&s=104
def main():
    stop = False
    while stop == False:
        vk_session = vk_api.VkApi(token=MyVKData_O.TOKEN)
        vk = vk_session.get_api()
        vk_session_wall = vk_api.VkApi(login=MyVKData_O.LOGIN, password=MyVKData_O.GET_PASSWORD)
        vk_session_wall.auth()
        vk_wall = vk_session_wall.get_api()
        fil_name = 'avito.csv'
        try:
            links = open_csv(fil_name)
        except FileNotFoundError:
            links=[]
        n1=len(links)
        base_url = 'https://www.avito.ru/sankt-peterburg/kvartiry/sdam/na_dlitelnyy_srok?'
        page_part = 'p='
        query_par =  '&user=1&s_trg=4&f=550_5702-5703-5704.501_5152b'
        url = base_url + page_part + '1' + query_par
        try:
            total_pages = get_total_pages(get_html(url))
        except:
            total_pages = get_total_pages(Proxy_next(url))
        # for i in range(1,int(total_pages)):
        for i in range(1, 10):
            url_gen = base_url + page_part + str(i) + query_par
            print(url_gen)
            try:
                html=get_html(url_gen)
            except:
                html = Proxy_next(url_gen)
            get_page_data(html,fil_name,links,vk,vk_wall)
            time.sleep(1)
        links = open_csv(fil_name)
        nn = len(links)
        print('Найдено ' + str(nn-n1) + ' новых объявлений')
        time.sleep(60*10)

if __name__ == '__main__':
    stop = False
    while stop == False:
        try:
            main()
        except Exception as e:
            logging.error(e, exc_info=True)
            time.sleep(60 * 10)
# if __name__ == '__main__':
#     main()
