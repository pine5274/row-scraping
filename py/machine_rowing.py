from unicodedata import category
from pandas.core import base
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import re
import pandas as pd

year_urls = [
    "https://www.jara.or.jp/mr/2000/",
    "https://www.jara.or.jp/mr/2001/",
    "https://www.jara.or.jp/mr/2002/",
    "https://www.jara.or.jp/mr/2003/",
    "https://www.jara.or.jp/mr/2004/",
    "https://www.jara.or.jp/mr/2005/",
    "https://www.jara.or.jp/mr/2006/",
    "https://www.jara.or.jp/mr/2007/",
    "https://www.jara.or.jp/mr/2008/",
    "https://www.jara.or.jp/mr/2009/",
    "https://www.jara.or.jp/mr/2010/",
    "https://www.jara.or.jp/mr/2011/",
    "https://www.jara.or.jp/mr/2012/",
    "https://www.jara.or.jp/mr/2013/",
    "https://www.jara.or.jp/mr/2014/",
    "https://www.jara.or.jp/mr/2015/",
    "https://www.jara.or.jp/mr/2016/",
    "https://www.jara.or.jp/mr/2017/",
    "https://www.jara.or.jp/mr/2018/",
    "https://www.jara.or.jp/mr/2019/",
]

class MrScrapingServise:
    __columns = ['year', 'block', 'sex', 'category', 'order', 'name', 'time', 'age', 'team']
    __dict = {}
    df = pd.DataFrame(columns=__columns)

    def __init__(self, year_urls) -> None:
        for url in tqdm(year_urls, desc='urls'):
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            blocks = [link.get('href') for link in soup.find('table', class_='table table-bordered table-condensed').find_all('a')]
            for block in blocks:
                # 総合順位はスクレイピングしない
                if re.search(r'\d\d\d\d[AB]', block):
                    self.scraping(url+block)

    def scraping(self, url):
        base_name = url[re.search(r'\/\d\d\d\d\/', url).end():]
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        categories = soup.find_all('div', class_='panel panel-default')
        for category in categories:
            self.__dict['year'] = base_name[:4]
            self.__dict['block'] = base_name[4:-7]
            self.__dict['sex'] = base_name[-6:-5]
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
        self.df.to_csv('../dst/machine_rowing.csv')

sc = MrScrapingServise(year_urls)
sc.export_csv()