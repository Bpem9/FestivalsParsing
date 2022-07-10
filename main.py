from bs4 import BeautifulSoup
import requests
import json
import pprint
import lxml
from pprint import pprint

URL = 'https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=&to_date=&maxprice=500&o=24&bannertitle=July'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36 OPR/88.0.4412.53',
    'accept':'*/*'
}
HOST = 'https://www.skiddle.com'
fest_list = []

def get_content(params=None):
    for i in range(0, 192, 24):
        url = f'https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=&to_date=&maxprice=500&o={i}&bannertitle=July'
        response = requests.get(url, params=params, headers=HEADERS)
        json_data = json.loads(response.text)
        html_data = json_data['html']
        with open (f'data/Index_{i}.html', 'w', encoding='utf-8') as file:
            file.write(html_data)
        print(f'{i} collected')
        sharing(i)
def sharing(i):
    with open(f'data/Index_{i}.html', 'r') as file:
        src = file.read()
    page_soup = BeautifulSoup(src, 'lxml')
    card_soup = page_soup.find_all('div', class_='card')

    urls_list = [HOST + card.find('a').get('href') for card in card_soup]

    for url in urls_list:
        try:
            url_res = requests.get(url, headers=HEADERS)
            url_soup = BeautifulSoup(url_res.text, 'lxml')
            fest_info_block = url_soup.find('div', class_='top-info-cont')
            fest_name = fest_info_block.find('h1').text
            fest_date = fest_info_block.find('h3').text
            fest_location_url =HOST + fest_info_block.find('a', class_='tc-white').get('href')
            fest_list.append({
                'Название':fest_name,
                'Локация':fest_location_url,
                'Дата':fest_date
            })
        except Exception as ex:
            print(f'Something went wrong... Look: *{ex}*')

    with open('result.json', 'a', encoding='utf-8') as file:
        json.dump(fest_list, file, indent=4, ensure_ascii=False)
    print(f'{i} shared')







if __name__ == '__main__':
    get_content()
