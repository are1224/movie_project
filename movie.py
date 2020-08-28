import requests
from bs4 import BeautifulSoup
import csv

# def get_news_soup_objects():
soup_objects = []

URL = 'https://movie.naver.com/movie/running/current.nhn'

response = requests.get(URL)
soup = BeautifulSoup(response.text, 'html.parser')

review_section = soup.select(
'div[id=container] > div[id=content] > div[class=article] > div[class=obj_section] > div[class=lst_wrap] > ul[class=lst_detail_t1] > li'
)



with open('movie7.csv', 'a', encoding='utf-8-sig', newline="") as csvfile:
    fieldname = ['title', 'id', 'genres']
    csvwriter = csv.DictWriter(csvfile, fieldname)
    csvwriter.writeheader()

    data_array = []

    for review in review_section:
            

            a_tag = review.select_one('dl > dt > a')

            review_title = a_tag.get_text()
            review_link = a_tag['href'].split('=')[1]

            data = {
                'title' : review_title,
                'id' : review_link,
                'genres' : []
            }
            genre_section = review.select('dl > dd:nth-child(3) > dl > dd:nth-child(2) > span.link_txt > a')

            for genre in genre_section:
                # print(genre.get_text())
                genre_id = genre['href'].split('=')[1]
                genre_text = genre.get_text()
                data['genres'].append({'id':genre_id, 'name': genre_text})
            print(data)
            # data_array.append([review_title, review_link])

            csvwriter.writerow(data)
    