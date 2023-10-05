l = []
d = {}
for links in tqdm(links_map, desc = 'list'):
    for link in tqdm(links, leave=False):
        base_name = link[re.search(r'\/\d\d\d\d\/|current/', link).end():]

        if not re.search(r'[wm]\d[x\-\+]', base_name):
            continue

        d_year = base_name[:4]
        d_boat_type = base_name[re.search(r'\_[wm]', base_name).start()+1:-5]

        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'lxml')
        race_results = soup.find_all('div', {'class': 'race-result'})
        
        for race_result in race_results:
            race_info = race_result.find('div', {'class': 'race-info'}).find_all('div')
            d_section_code = race_info[1].find('a').text
            race_number = race_result.find('div', {'class': 'panel-heading'}).text
            d_race_number = re.search(r'\d+', race_number).group()
            if int(d_year) < 2020:
                rows = race_result.find_all('tr')
                for i in range(len(rows)-1):
                    tds = rows[i+1].find_all('td')
                    d['year']         = d_year
                    d['boat_type']    = d_boat_type
                    d['section_code'] = d_section_code
                    d['race_number']  = d_race_number
                    d['order']        = tds[0].text
                    d['team']         = tds[1].text
                    d['500m']         = tds[2].text
                    d['1000m']        = tds[3].text
                    d['1500m']        = tds[4].text
                    d['2000m']        = tds[5].text
                    d['lane']         = tds[6].text
                    d['qualify']      = tds[7].text
                    l.append(d)
                    d = {}
            else:
                table = race_result.find(('table'))
                for t in table.find_all('tr', {'class': 'collapse'}):
                    t.decompose()
                rows = table.find_all('tr')
                for i in range(len(rows)-1):
                    tds = rows[i+1].find_all('td')
                    d['year']         = d_year
                    d['boat_type']    = d_boat_type
                    d['section_code'] = d_section_code
                    d['race_number']  = d_race_number
                    d['order']        = tds[0].text
                    d['team']         = tds[1].text
                    d['500m']         = tds[2].text
                    d['1000m']        = tds[3].text
                    d['1500m']        = tds[4].text
                    d['2000m']        = tds[5].text
                    d['lane']         = tds[6].text
                    d['qualify']      = tds[7].text
                    l.append(d)
                    d = {}

df = pd.DataFrame(l)
df.to_csv('./../dst/inter_college_2023.csv')