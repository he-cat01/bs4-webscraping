# -*- coding: utf8 -*-
import sys
import re
import csv
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool, cpu_count
from datetime import datetime
from fake_useragent import UserAgent


def save_csv(data_base):
    with open(f'dump_kolesa_{datetime.now().date()}.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',')
        write_csv = (data_base['title'], data_base['city'], data_base['price'], data_base['phone'], data_base['link'])
        writer.writerow(write_csv)


def get_page(URL: str) -> str:
    page = requests.get(URL, headers={'User-Agent': UserAgent(verify_ssl=False).random})
    soup = BeautifulSoup(page.content, 'lxml')
    return soup


def get_data(soup: str) -> csv:
    headers_phone = {
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': UserAgent(verify_ssl=False).random
    }

    table = soup.find_all(class_=re.compile('row vw-item list-item'))

    for item in table:
        title = item.select('.a-el-info-title')[0].get_text(strip=True)
        link = 'https://kolesa.kz' + item.select('span.a-el-info-title')[0].find('a').get('href')
        price = item.select('.price')[0].get_text(strip=True)
        city = item.select('div.list-region')[0].get_text(strip=True)
        try:
            link_phone = 'https://kolesa.kz' + get_page(link).select('.offer__show-phone')[0].get('data-href')
            session = requests.session().get(link_phone, headers=headers_phone).json()['phones']
            phone = '; '.join(session)
        except:
            phone = ''

        data_base = {'title': title, 'city': city, 'price': price, 'phone': phone, 'link': link}
        save_csv(data_base)

def make_all(pattern: str):
    get_data(get_page(pattern))


def main(pattern, threads=cpu_count()):
    pattern += '?page={}'
    last_page = get_page(pattern).select('.pager')[0].find_all('li')[-1].get_text(strip=True)
    urls = [pattern.format(str(i)) for i in range(1, int(last_page) + 1)]

    with Pool(threads) as p:
        p.map(make_all, urls)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        main(sys.argv[1], int(sys.argv[2]))
    else:
        main(sys.argv[1])