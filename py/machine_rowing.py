from unicodedata import category
from pandas.core import base
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import re
import pandas as pd

class MrScrapingServise:
    __columns = ['year', 'block', 'sex', 'category', 'order', 'name', 'time', 'age', 'team']
    df = pd.DataFrame(columns=__columns)
    __dict = {}

    def __init__(self, url_list) -> None:
        for url in tqdm(url_list, desc='list'):
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'lxml')
            links = [link.get('href') for link in soup.find('table', class_='table table-bordered table-condensed').find_all('a')]
            for link in tqdm(links, leave=False):
                if re.search(r'\d\d\d\d[AB]', link):
                    self.scraping(url+link)

    def scraping(self, url):
        base_name = url[re.search(r'\/\d\d\d\d\/', url).end():]
        self.__dict['year'] = base_name[:4]
        self.__dict['block'] = base_name[4:-7]
        self.__dict['sex'] = base_name[-6:-5]
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'lxml')
        categories = soup.find_all('div', class_='panel panel-default')
        for category in categories:
            self.__dict['category'] = category.find('div', class_='panel-heading').text
            self.scraping_table_data(category.find('table', class_='table'))
        
    def scraping_table_data(self, table):
        rows = table.find_all('tr')
        for i in range(len(rows)-1):
            tds = rows[i+1].find_all('td')
            self.__dict['order'] = tds[0].text
            self.__dict['name']  = tds[1].text
            self.__dict['time']  = tds[2].text
            self.__dict['age']   = tds[3].text
            self.__dict['team']  = tds[4].text
            self.df = self.df.append(pd.Series(self.__dict.values(), index=self.__dict.keys()), ignore_index=True)

    def print_df(self):
        print(self.df)

    def export_csv(self):
        self.df.to_csv('machine_rowing.csv')

url = "https://www.jara.or.jp/mr/2019/2019A_kantou_M.html"
url_list = [
    "https://www.jara.or.jp/mr/2011/",
    # "https://www.jara.or.jp/mr/2012/",
    # "https://www.jara.or.jp/mr/2013/",
    # "https://www.jara.or.jp/mr/2014/",
    # "https://www.jara.or.jp/mr/2015/",
    # "https://www.jara.or.jp/mr/2016/",
    # "https://www.jara.or.jp/mr/2017/",
    # "https://www.jara.or.jp/mr/2018/",
    # "https://www.jara.or.jp/mr/2019/",
]
sc = MrScrapingServise(url_list)
sc.export_csv()