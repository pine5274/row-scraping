import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import re
import pandas as pd

year_urls = [
    "https://www.jara.or.jp/race/current/2023intercollege.html",
]

# years = list(range(2000, 20))
# BASE_URL = "https://www.jara.or.jp/race/"
# BASE_HTML = "intercollege.html"

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
            links_list = list(map(lambda x: url[:re.search(r'current/', url).end()] + x, links_list))
            self.__links_lists.append(links_list)

    def scraping(self):
        for links_list in tqdm(self.__links_lists, desc = 'list'):
            for link in tqdm(links_list, leave=False):
                base_name = link[re.search(r'current/', link).end():]

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

sc.scraping()
df = sc.df
df[df['2000m'] != ''].to_csv('inter_college_2023.csv')