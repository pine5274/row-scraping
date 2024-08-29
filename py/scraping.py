import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import re
import pandas as pd

def time_to_sec(x):
    if (type(x) is float):
        return x
    if (x == ''):
        return x
    minutes = int(x[1])
    seconds = float(x[-5:])
    return minutes * 60 + seconds

url = "https://www.jara.or.jp/race/current/2024alljapan.html"

node = url[:re.search(r'\d{4}[a-z]+\.html', url).start()]
page = requests.get(url)
soup = BeautifulSoup(page.content, 'lxml')
links = [link.get('href') for link in soup.find('table', {'id': 'event'}).find_all('a')]
links = list(map(lambda x: node + x, links))

l = []
d = {}

for link in tqdm(links):
    year = re.search(r'\d{4}', link).group()
    boat_type = re.search(r'(\d{4}.+_)(.+)(\.html)', link).group(2)

    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'lxml')
    race_results = soup.find_all('div', {'class': 'race-result'})

    for race_result in race_results:
        race_info = race_result.find('div', {'class': 'race-info'}).find_all('div')
        section_code = race_info[1].find('a').text
        race_number = race_result.find('div', {'class': 'panel-heading'}).text
        race_number = re.search(r'\d+', race_number).group()

        if int(year) < 2020:
            rows = race_result.find_all('tr')
            for i in range(len(rows)-1):
                tds = rows[i+1].find_all('td')
                d['year']         = year
                d['nace_number']  = race_number
                d['boat_type']    = boat_type
                d['section_code'] = section_code
                d['lane']         = tds[6].text
                d['team']         = tds[1].text
                d['500m']         = tds[2].text
                d['1000m']        = tds[3].text
                d['1500m']        = tds[4].text
                d['2000m']        = tds[5].text
                d['500m(s)']      = time_to_sec(tds[2].text)
                d['1000m(s)']     = time_to_sec(tds[3].text)
                d['1500m(s)']     = time_to_sec(tds[4].text)
                d['2000m(s)']     = time_to_sec(tds[5].text)
                d['order']        = tds[0].text
                d['qualify']      = tds[7].text
                l.append(d)
                d = {}
        else:
            race_table = race_result.find(('table'))
            for t in race_table.find_all('tr', {'class': 'collapse'}):
                t.decompose()
            rows = race_table.find_all('tr')
            for i in range(len(rows)-1):
                tds = rows[i+1].find_all('td')
                d['year']         = year
                d['nace_number']  = race_number
                d['boat_type']    = boat_type
                d['section_code'] = section_code
                d['lane']         = tds[6].text
                d['team']         = tds[1].text
                d['500m']         = tds[2].text
                d['1000m']        = tds[3].text
                d['1500m']        = tds[4].text
                d['2000m']        = tds[5].text
                d['500m(s)']      = time_to_sec(tds[2].text)
                d['1000m(s)']     = time_to_sec(tds[3].text)
                d['1500m(s)']     = time_to_sec(tds[4].text)
                d['2000m(s)']     = time_to_sec(tds[5].text)
                d['order']        = tds[0].text
                d['qualify']      = tds[7].text
                l.append(d)
                d = {}

df = pd.DataFrame(l)
df = df.dropna(subset=['2000m'])
df = df[df['2000m'] != '']