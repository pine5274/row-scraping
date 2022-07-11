import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import re
import pandas as pd

year_urls = [
    "https://www.jara.or.jp/race/2000/2000intercollege.html",
    "https://www.jara.or.jp/race/2001/2001intercollege.html",
    "https://www.jara.or.jp/race/2002/2002intercollege.html",
    "https://www.jara.or.jp/race/2003/2003intercollege.html",
    "https://www.jara.or.jp/race/2004/2004intercollege.html",
    "https://www.jara.or.jp/race/2005/2005intercollege.html",
    "https://www.jara.or.jp/race/2006/2006intercollege.html",
    "https://www.jara.or.jp/race/2006/2006intercollege.html",
    "https://www.jara.or.jp/race/2007/2007intercollege.html",
    "https://www.jara.or.jp/race/2008/2008intercollege.html",
    "https://www.jara.or.jp/race/2009/2009intercollege.html",
    "https://www.jara.or.jp/race/2010/2010intercollege.html",
    "https://www.jara.or.jp/race/2011/2011intercollege.html",
    "https://www.jara.or.jp/race/2012/2012intercollege.html",
    "https://www.jara.or.jp/race/2013/2013intercollege.html",
    "https://www.jara.or.jp/race/2014/2014intercollege.html",
    "https://www.jara.or.jp/race/2015/2015intercollege.html",
    "https://www.jara.or.jp/race/2016/2016intercollege.html",
    "https://www.jara.or.jp/race/2017/2017intercollege.html",
    "https://www.jara.or.jp/race/2018/2018intercollege.html",
    "https://www.jara.or.jp/race/2019/2019intercollege.html",
    "https://www.jara.or.jp/race/2020/2020intercollege.html",
    # "https://www.jara.or.jp/race/2021/2021intercollege.html"
]

years = list(range(2000, 20))
BASE_URL = "https://www.jara.or.jp/race/"
BASE_HTML = "intercollege.html"

class RaceScrapingServise:
    __columns = ['year', 'race_number', 'boat_type', 'section_code', 'lane', 'team', '500m', '1000m', '1500m', '2000m', 'order', 'qualify']
    df = pd.DataFrame(columns=__columns)
    __dict = {}
    __links_lists =[]

    def __init__(self, year_urls):
        for url in year_urls:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'lxml')
            links_list = [link.get('href') for link in soup.find('table', {'id': 'event'}).find_all('a')]
            links_list = list(map(lambda x: url[:re.search(r'\d\d\d\d\/', url).end()] + x, links_list))
            self.__links_lists.append(links_list)

    def scraping(self):
        for links_list in tqdm(self.__links_lists, desc = 'list'):
            for link in tqdm(links_list, leave=False):
                base_name = link[re.search(r'\/\d\d\d\d\/', link).end():]

                if not re.search(r'[wm]\d[x\-\+]', base_name):
                    continue

                self.__dict['year'] = base_name[:4]
                self.__dict['boat_type'] = base_name[re.search(r'\_[wm]', base_name).start()+1:-5]

                page = requests.get(link)
                soup = BeautifulSoup(page.content, 'lxml')
                race_results = soup.find_all('div', {'class': 'race-result'})
                self.scraping_race_results(race_results)

    def scraping_race_results(self, race_results):
        for race_result in race_results:
            race_info = race_result.find('div', {'class': 'race-info'}).find_all('div')
            self.__dict['section_code'] = race_info[1].find('a').text
            race_number = race_result.find('div', {'class': 'panel-heading'}).text
            self.__dict['race_number'] = re.search(r'\d+', race_number).group()
            if int(self.__dict['year']) >= 2020:
                self.scraping_table_data_2020(race_result)
            else:
                self.scraping_table_data(race_result.find(('table')))

    def scraping_table_data(self, table):
        rows = table.find_all('tr')
        for i in range(len(rows)-1):
            tds = rows[i+1].find_all('td')
            self.__dict['order']   = tds[0].text
            self.__dict['team']    = tds[1].text
            self.__dict['500m']    = tds[2].text
            self.__dict['1000m']   = tds[3].text
            self.__dict['1500m']   = tds[4].text
            self.__dict['2000m']   = tds[5].text
            self.__dict['lane']    = tds[6].text
            self.__dict['qualify'] = tds[7].text
            self.df = self.df.append(pd.Series(self.__dict.values(), index=self.__dict.keys()), ignore_index=True)

    def scraping_table_data_2020(self, table):
        for t in table.find_all('tr', {'class': 'collapse'}):
            t.decompose()
        rows = table.find_all('tr')
        for i in range(len(rows)-1):
            tds = rows[i+1].find_all('td')
            self.__dict['order']   = tds[0].text
            self.__dict['team']    = tds[1].text
            self.__dict['500m']    = tds[2].text
            self.__dict['1000m']   = tds[3].text
            self.__dict['1500m']   = tds[4].text
            self.__dict['2000m']   = tds[5].text
            self.__dict['lane']    = tds[6].text
            self.__dict['qualify'] = tds[7].text
            self.df = self.df.append(pd.Series(self.__dict.values(), index=self.__dict.keys()), ignore_index=True)

    def export_csv(self):
        self.df.to_csv('race_scraping2021.csv')

sc = RaceScrapingServise(year_urls)

# リファクタリング中
def fetch_years_category_urls(years):
    dict = {}
    for year in years:
        url = BASE_URL + str(year) + "/" + str(year) + BASE_HTML
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'lxml')
        categories = [link.get('href') for link in soup.find('table', {'id': 'event'}).find_all('a')]
        dict[str(year)] = categories
    return dict

def scraping(year_dict):
    dict = {}
    for key, value in tqdm(year_dict.items(), desc = 'list'):
        for category in value:
            # OX盾や総合順位は省く
            if not re.search(r'[wm]\d[x\-\+]', category):
                continue
            url = BASE_URL + key + "/" + value
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'lxml')
            race_results = soup.find_all('div', {'class': 'race-result'})

# def scrapingRaceResults(race_results):


years = list(range(2000, 2020))
year_dict = fetch_years_category_urls(years)
for key, value in tqdm(year_dict.items(), desc = 'list'):

columns = ['year', 'race_number', 'boat_type', 'section_code', 'lane', 'team', '500m', '1000m', '1500m', '2000m', 'order', 'qualify']
df = pd.DataFrame(columns=columns)
BASE_URL = "https://www.jara.or.jp/race/"
year_dict = {}

for year in years:
    url = BASE_URL + str(year) + "/" + str(year) + BASE_HTML
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    categories = [link.get('href') for link in soup.find('table', {'id': 'event'}).find_all('a')]
    year_dict[str(year)] = categories

dict = {}
for key, value in tqdm(dict.items(), desc = 'list'):
    for category in value:
        # OX盾や総合順位は省く
        if not re.search(r'[wm]\d[x\-\+]', category):
            continue
        url = BASE_URL + key + "/" + value
        soup = BeautifulSoup(page.content, 'lxml')
        race_results = soup.find_all('div', {'class': 'race-result'})

        # dict['year'] = key
        # dict['boat_type'] = category[re.search(r'\_[wm]', category).start()+1:-5]

print(dict)