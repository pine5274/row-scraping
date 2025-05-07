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

def extract_year_from_url(url):
    """URLから4桁の年を抽出する"""
    match = re.search(r'/(\d{4})/', url)
    return match.group(1) if match else None

def extract_boat_type_from_href(href):
    """hrefからボートタイプを抽出する"""
    match = re.search(r'_(.*?)\.html', href)
    return match.group(1) if match else None

def get_base_url(url):
    """URLからベースURLを抽出する"""
    match = re.match(r'(.*/)\d{4}.*\.html$', url)
    return match.group(1) if match else None

def fetch_html(url):
    """指定されたURLからHTMLを取得する"""
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    return response.text

def parse_event_table(soup):
    """イベントテーブルからリンクリストを取得する"""
    event_table = soup.find('table', {'id': 'event'})
    if not event_table:
        return []
    links = event_table.find_all('a', href=True)
    return [link['href'] for link in links]

def clean_rows(rows):
    """class='collapse' を持つ <tr> 要素を削除"""
    for row in rows.find_all('tr', {'class': 'collapse'}):
        row.decompose()
    return rows.find_all('tr')

def extract_race_data(rows, year, race_number, boat_type, section_code):
    """レースデータを辞書形式で抽出"""
    data_list = []
    for row in rows[1:]:  # ヘッダー行をスキップ
        cols = row.find_all('td')
        if len(cols) < 8:
            continue
        race_data = {
            'year': year,
            'race_number': race_number,
            'boat_type': boat_type,
            'section_code': section_code,
            'lane': cols[0].text.strip(),
            'team': cols[1].text.strip(),
            'Q1': cols[2].text.strip(),
            'Q2': cols[3].text.strip(),
            'Q3': cols[4].text.strip(),
            'Q4': cols[5].text.strip(),
            'order': cols[6].text.strip(),
            'qualify': cols[7].text.strip(),
            'Q1[s]': time_to_sec(cols[2].text.strip()),
            'Q2[s]': time_to_sec(cols[3].text.strip()),
            'Q3[s]': time_to_sec(cols[4].text.strip()),
            'Q4[s]': time_to_sec(cols[5].text.strip()),
        }
        data_list.append(race_data)
    return data_list

# メイン処理
url = "https://www.jara.or.jp/race/2024/2024alljapan.html"
base_url = get_base_url(url)
if not base_url:
    print("URLの形式が正しくありません。")
    exit()

html = fetch_html(url)
soup = BeautifulSoup(html, 'html.parser')
href_list = parse_event_table(soup)

if not href_list:
    print("href_list が空です。")
    exit()
# href_list のすべてのリンクを処理
data_list = []  # 全データを格納するリスト

for href in tqdm(href_list, desc="Processing href_list"):
    # 各リンクの完全URLを作成
    full_url = base_url + href
    print(f"アクセスするURL: {full_url}")

    # HTMLを取得して解析
    html_race = fetch_html(full_url)
    soup_race = BeautifulSoup(html_race, 'html.parser')
    race_results = soup_race.find_all('div', class_='race-result')

    # 各レース結果を処理
    for result in race_results:
        # レース情報を取得
        race_info = result.find('div', class_='race-info')
        section_code = race_info.find('a').text.strip() if race_info else None

        # レース番号を取得
        panel_heading = result.find('div', class_='panel-heading')
        race_number = re.search(r'\d+', panel_heading.text).group() if panel_heading else None

        # テーブルデータを取得
        result_table = result.find('table')
        if result_table:
            rows = clean_rows(result_table)
            year = extract_year_from_url(url)
            boat_type = extract_boat_type_from_href(href)
            race_data = extract_race_data(rows, year, race_number, boat_type, section_code)
            data_list.extend(race_data)

    # 5秒間隔を設ける
    time.sleep(5)

# データをデータフレームに変換
df = pd.DataFrame(data_list)

# データフレームを確認
print(df)

# 必要に応じてCSVファイルに保存
df.to_csv('race_results.csv', index=False, encoding='utf-8-sig')