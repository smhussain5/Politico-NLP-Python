"""
Terminal application scrapes Politico website for articles to summarize
"""

from bs4 import BeautifulSoup as bs
from colorama import Fore, Style, init, deinit
from newspaper import Article
from pyfiglet import Figlet
from textblob import TextBlob
import nltk
import requests

init()  # INITIALIZE COLORAMA

nltk.download("punkt")  # DOWNLOAD NLTK PUNKT TOKENIZER

fig = Figlet(font="isometric1")  # WELCOME SCREEN
print(fig.renderText("NEWS"))
print("One moment while your news loads!")
print("...")

URL = "https://www.politico.com/"  # CONVERT URL TO BEAUTIFULSOUP OBJECT
rqst = requests.get(URL, timeout=120)
soup = bs(rqst.content, features="lxml")

working_div = soup.find(
    "div", class_="container__row layout--fluid-fixed"
)  # FIND DIV CONTAINING "TOP NEWS"

all_headings = working_div.select("h3 a")  # COLLECT H3 TAGS FROM WORKING DIV

article_links = []  # COLLECT HREF LINKS FROM H3 TAGS
for heading in all_headings:
    article_links.append(heading["href"])

article_objects = {}  # COLLECT ARTICLE INFORMATION FROM HREF LINKS
for link in article_links:
    article = Article(link)
    article.download()
    article.parse()
    article.nlp()
    if (
        article.title and article.summary
    ):  # COLLECT INFORMATION ONLY IF ARTICLE TITLES AND SUMMARIES EXISTS
        analysis = TextBlob(article.text)
        article_score = round(analysis.polarity * 100, 2)  # CALCULATE POLARITY SCORE
        article_objects[article.title] = [article.summary, article_score]

for (
    key,
    value,
) in article_objects.items():  # DISPLAY EVERY ARTICLE SUMMARY + POLARITY SCORE
    print(Fore.GREEN)
    print(f"{key.upper()} (POLARITY: {value[1]}%)")
    print(Style.RESET_ALL)
    print(f"{value[0]}\n")

deinit()  # DE-INITIALIZE COLORAMA
input("Happy reading! Press ENTER to exit.")  # EXIT APPLICATION
