from bs4 import BeautifulSoup
import requests
import time

class Avito:
    def __init__(self, main_url):
        self.main_url = main_url
        first_url = self.get_url( 1)
        soup = self.get_soup(first_url)
        self.total_pages = self.get_total_pages(soup)
        self.main_cycle()

    def main_cycle(self):
        for i in range(1, self.total_pages):
            url = self.get_url(i)
            soup = self.get_soup(url)
            print(soup)
            time.sleep(0.5)


    def get_url(self, nom_list):
        base_url = self.main_url
        page_part = 'p='
        query_par = '&user=1&s_trg=4&f=550_5702-5703-5704.501_5152b'
        return f"{base_url}{page_part}{nom_list}{query_par}"


    def get_total_pages(self, soup):
        pages = soup.find('div', class_='pagination-pages clearfix').find_all('a', class_='pagination-page')[-1].get('href')
        total_pages = pages.split('=')[1].split('&')[0]
        return int(total_pages)


    def get_soup(self, url):
        return BeautifulSoup(requests.get(url).text, 'lxml')


if __name__ == '__main__':
    Avito('https://www.avito.ru/sankt-peterburg/kvartiry/sdam/na_dlitelnyy_srok?')