import requests
from bs4 import BeautifulSoup as bs
import nltk
from newspaper import Article
from textblob import TextBlob
from colorama import Fore, Style, init, deinit

init()

nltk.download("punkt")

url = "https://www.politico.com/"

rqst = requests.get(url)

soup = bs(rqst.content, features="lxml")

working_div = soup.find("div", class_="container__row layout--fluid-fixed")

all_headings = working_div.select("h3 a")

article_links = []

for heading in all_headings:
    article_links.append(heading["href"])


article_objects = {}
for link in article_links:
    article = Article(link)
    article.download()
    article.parse()
    article.nlp()
    if article.title and article.summary:
        analysis = TextBlob(article.text)
        article_score = round(analysis.polarity*100, 2)
        article_objects[article.title] = [article.summary, article_score]

for key, value in article_objects.items():
    print(Fore.GREEN)
    print(f"{key.upper()} (POLARITY: {value[1]}%)")
    print(Style.RESET_ALL)
    print(f"{value[0]}\n")

deinit()
input("Happy reading! Press ENTER to exit.")
