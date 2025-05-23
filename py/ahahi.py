import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import re
import pandas as pd
import time

def time_to_sec(x):
    """時間を秒に変換し、小数点以下1桁に四捨五入する"""
    if isinstance(x, float):
        return round(x, 1)
    if x == '':
        return x
    time = x.split(':')
    minutes = int(time[0])
    seconds = float(time[1])
    return round(minutes * 60 + seconds, 1)

def parse_event_table(soup):
    """イベントテーブルからリンクリストを取得する"""
    event_table = soup.find('tr')
    if not event_table:
        return []
    links = event_table.find_all('a', href=True)
    return [link['href'] for link in links]

def get_base_url(url):
    """URLからベースURLを抽出する"""
    match = re.match(r'(.*/).*\.htm$', url)
    return match.group(1) if match else None

def fetch_html(url):
    """指定されたURLからHTMLを取得する"""
    response = requests.get(url)
    response.encoding = 'shift_jis'  # 文字コードを指定
    return response.text

# メイン処理
url = "https://karal.jp/news_flash75a/result.htm"
base_url = get_base_url(url)
if not base_url:
    print("URLの形式が正しくありません。")

html = fetch_html(url)
soup = BeautifulSoup(html, 'html.parser')
href_list = parse_event_table(soup)

# href_list の先頭10個だけを残す
href_list = href_list[:10]

# 確認のため出力
print(f"先頭10個のリンク: {href_list}")

if not href_list:
    print("href_list が空です。")
data_list = []  # 全データを格納するリスト

for href in tqdm(href_list, desc="Processing href_list"):
    # 各リンクの完全URLを作成
    full_url = base_url + href
    print(f"アクセスするURL: {full_url}")

    # HTMLを取得して解析
    html_race = fetch_html(full_url)
    soup_race = BeautifulSoup(html_race, 'html.parser')
    race_results = soup_race.find('table')

    race_info = ''
    match = re.search(r'result/result(.*?)\.htm', href)
    boat_type = match.group(1)
    rows = race_results.find_all('tr')

    for i, row in enumerate(rows):
        cols = row.find_all('td')
        if i % 7 == 0:
            continue
        elif i % 7 == 1:
            td_with_rowspan = row.find('td', {'rowspan': '6'})
            if td_with_rowspan:
                race_info = td_with_rowspan.text.strip()
                match = re.search(r'\d:\d{2}(.*)', race_info)
                race_info =  match.group(1).strip()
            race_data = {
                # 'race_number': race_number,
                'boat_type': boat_type,
                'race_info': race_info,
                'BNo.': cols[1].text.strip(),
                'team': cols[2].text.strip(),
                '500m': cols[3].text.strip(),
                '1000m': cols[4].text.strip(),
                'order': cols[5].text.strip(),
                '100': '',
                '200': '',
                '300': '',
                '400': '',
                '500': time_to_sec(cols[3].text.strip()),
                '600': '',
                '700': '',
                '800': '',
                '900': '',
                '1000': time_to_sec(cols[4].text.strip()),
            }
        else:
            race_data = {
                # 'race_number': race_number,
                'boat_type': boat_type,
                # 'section_code': section_code,
                'race_info': race_info,
                'BNo.': cols[0].text.strip(),
                'team': cols[1].text.strip(),
                '500m': cols[2].text.strip(),
                '1000m': cols[3].text.strip(),
                'order': cols[4].text.strip(),
                '100': '',
                '200': '',
                '300': '',
                '400': '',
                '500': time_to_sec(cols[2].text.strip()),
                '600': '',
                '700': '',
                '800': '',
                '900': '',
                '1000': time_to_sec(cols[3].text.strip()),
            }

        data_list.append(race_data)
        
    time.sleep(3)


# # データをデータフレームに変換
df = pd.DataFrame(data_list)

# # データフレームを確認
print(df)

# # 必要に応じてCSVファイルに保存
# df.to_csv('race_results.csv', index=False, encoding='utf-8-sig')