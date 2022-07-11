import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import re

def fetch_soup(url):
    return BeautifulSoup(requests.get(url).content, 'lxml')
    
def make_href_list(soup, selector):
    return [url.get('href') for url in soup.select_one(selector).find_all('a')]

def crawling(root_url):
    links = make_href_list(fetch_soup(root_url), 'ul.list-group')
    dict = {}
    for link in tqdm(links):
        url = root_url + link[2:]
        l = make_href_list(fetch_soup(url), 'body')
        l = list(filter(lambda x: x != None, l))
        l = [url + s for s in l if '.html' in s]
        dict[url] = l

    urls = []
    for k, v in tqdm(dict.items()):
        for url in v:
            l = make_href_list(fetch_soup(url), 'body')
            l = list(filter(lambda x: x != None, l))
            l = [k + s for s in l if re.match('[0-9]{4}.*[wm][1-8][\-\+x].html', s)]
            urls.extend(l)
    
    return urls