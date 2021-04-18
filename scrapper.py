from bs4 import BeautifulSoup
import requests

URL = ""
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

#print(soup.find_all('a')[0].find(class_="title").string)
content = soup.find(id="list_videos_most_recent_videos_items")

#print(content)
videos = content.find_all('a')

for video in videos:
    title = video.find(class_="title").get_text()

    a_list = title.split()

    title = " ".join(a_list)

    print(title)
