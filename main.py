
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import json

def get_first_news():

    list_card_url = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'}

    url = 'https://kazan.mk.ru/news/'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    date = soup.find_all('li', class_='news-listing__item')

    for i in date:
        card_url = i.find('a').get('href')
        list_card_url.append(card_url)

    news_dict = {}
    for card_url in list_card_url:
        responses = requests.get(card_url, headers=headers)
        soups = BeautifulSoup(responses.text, 'lxml')
        data = soups.find('div', class_='wraper__content')

        article_text = data.find('div', class_='article__body').text
        article_name = data.find('h1', class_='article__title').text
        article_date_time = data.find("time").get("datetime")
        date_from_iso = datetime.fromisoformat(article_date_time)
        date_time = datetime.strftime(date_from_iso, "%Y-%m-%d %H:%M:%S.%f")
        article_date_timestamp = time.mktime(datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S.%f").timetuple())

        article_id = card_url.rsplit('/', 1)[-1]
        article_id = article_id[:-5]

        news_dict[article_id] = {
            "article_date_timestamp": article_date_timestamp,
            "card_url": card_url,
            "article_name": article_name,
            "article_text": article_text
        }
        with open("news_dict.json", "w", encoding="utf-8") as file:
            json.dump(news_dict, file, indent=4, ensure_ascii=False)


def check_news_update():
    with open('news_dict.json', encoding='utf-8') as file:
        news_dict = json.load(file)
    # print(news_dict)


    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'}

    url = 'https://kazan.mk.ru/news/'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    date = soup.find_all('li', class_='news-listing__item')


    # print(list_card_url)

    fresh_news = {}
    list_card_url = []

    for i in date:
        card_url = i.find('a').get('href')
        article_id = card_url.rsplit('/', 1)[-1]
        article_id = article_id[:-5]

        if article_id in news_dict:
            continue
        else:
            url = 'https://kazan.mk.ru/news/'
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            date = soup.find_all('li', class_='news-listing__item')

            card_url = i.find('a').get('href')
            list_card_url.append(card_url)

            responses = requests.get(card_url, headers=headers)
            soups = BeautifulSoup(responses.text, 'lxml')
            data = soups.find('div', class_='wraper__content')

            article_text = data.find('div', class_='article__body').text
            article_name = data.find('h1', class_='article__title').text
            article_date_time = data.find("time").get("datetime")
            date_from_iso = datetime.fromisoformat(article_date_time)
            date_time = datetime.strftime(date_from_iso, "%Y-%m-%d %H:%M:%S.%f")
            article_date_timestamp = time.mktime(datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S.%f").timetuple())

            news_dict[article_id] = {
                "article_date_timestamp": article_date_timestamp,
                "card_url": card_url,
                "article_name": article_name,
                "article_text": article_text
            }
            fresh_news[article_id] = {
                "article_date_timestamp": article_date_timestamp,
                "card_url": card_url,
                "article_name": article_name,
                "article_text": article_text
            }
            # print(f"{article_name} | {article_text} | {article_date_timestamp}")
        with open("news_dict.json", "w", encoding="utf-8") as file:
            json.dump(news_dict, file, indent=4, ensure_ascii=False)

        return fresh_news



def main():
    # get_first_news()
   check_news_update()




if __name__ == '__main__':
     main()

