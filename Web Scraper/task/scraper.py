import os
import re
import string
import requests
from bs4 import BeautifulSoup


number_pages = int(input())
article_type = input()

# https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&type=news&year=2020&page=2
input_url = "https://www.nature.com"


for i in range(1, number_pages+1):
    r = requests.get(f"{input_url}/nature/articles?sort=PubDate&year=2020&page={i}")

    soup = BeautifulSoup(r.text, "html.parser")
    articles = soup.find_all("article")

    try:
        os.mkdir(f"Page_{i}")
    except FileExistsError:
        pass

    os.chdir(f"Page_{i}")

    for child in articles:
        news_check = child.find("span", attrs={"class": "c-meta__type"}).get_text()

        if news_check is not None and news_check == article_type:
            is_news = True
            article_detail = child.find("a", attrs={"data-track-action": "view article"})
            temp_title = article_detail.get_text().strip(" ")

            article_title = re.sub(f"[{string.punctuation}\s’‘—]+", "_", temp_title, count=500)
            # article_title = article_title.translate(str.maketrans(string.punctuation, ''*len(string.punctuation)))

            # load the article body
            r_article = requests.get(f"{input_url}{article_detail['href']}")
            article_soup = BeautifulSoup(r_article.text, "html.parser")
            body = article_soup.find("div", attrs={"class": "c-article-body main-content"})

            if body is not None:
                with open(f"{article_title}.txt", "wb") as file:
                    file.write(bytes(body.text.strip(" "), "utf-8"))
                print(f"Saved at {os.path.join(os.getcwd(), f'{article_title}.txt')}")
    os.chdir("..")

print("Saved all articles.")
