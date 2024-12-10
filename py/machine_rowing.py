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
    time = x.split(':')
    minutes = int(time[0][1])
    seconds = float(time[1])
    return minutes * 60 + seconds

urls = [
    "https://www.jara.or.jp/mr/current/index.html"
]

# url = "https://www.jara.or.jp/race/current/2024alljapan.html"

l = []
d = {}

# current
for url in urls:
    root = "https://www.jara.or.jp/mr/current/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    links = [link.get('href') for link in soup.find('table', {'id': 'JaraMr'}).find_all('a')]
    del links[-8:]
    links = list(map(lambda x: root + x, links))

    for link in tqdm(links):
        year = re.search(r'\d{4}', link).group()

        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'lxml')
        title = soup.find('h1', {'class': 'title'}).text
        region = re.search(r'－.+－', title).group()
        region = region[1:-1]
        print(title)
        sex = re.search(r'－.*$', title).group()
        sex = sex[-2:]

        categories = soup.find_all('div', {'class': 'panel-default'})

        for race_result in categories:
            category = race_result.find('div', {'class': 'panel-heading'}).text

            rows = race_result.find_all('tr')
            for i in range(len(rows)-1):
                tds = rows[i+1].find_all('td')
                d['year']         = year
                d['region']         = region
                d['sex']         = sex
                d['category'] = category
                d['rank']         = tds[0].text
                d['name']         = tds[1].text
                d['age']         = tds[3].text
                d['time']        = tds[2].text
                d['time(s)']     = time_to_sec(tds[2].text)
                d['team']         = tds[4].text
                l.append(d)
                d = {}

df = pd.DataFrame(l)
