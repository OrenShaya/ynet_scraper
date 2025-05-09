from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime
import requests
from bs4 import BeautifulSoup

@dataclass
class ArticleData:
    title: str
    author: Optional[str]
    publication_date: Optional[datetime]
    content: str
    image_urls: List[str]

    def __repr__(self):
        return (f"Title: {self.title}\n"
                f"Author: {self.author}\nPublished date: {self.publication_date}\n"
                f"The article has {len(self.image_urls)} images\n"
                f"The article has {len(self.content.split(' '))} words\n")

def scrape_ynet_articles(urls: List[str]) -> List[ArticleData]:
    """
    Given a list of YNET article URLs, return a list of ArticleData objects
    containing the extracted information from each article.
    :param urls: List of URLs pointing to YNET articles.
    :return: List of ArticleData objects.
    """
    articles_list: List[ArticleData] = []
    for link in urls:
        try:
            r = requests.get(link)
            soup = BeautifulSoup(r.content, 'html5lib')
        except:
            print("Error getting url")

        try:
            title: str = soup.find("h1", "mainTitle").text
            # print(title)
        except AttributeError:
            print("main title was not found")
            title = "Unknown title"

        author_div = soup.find("div", "authors")
        try:
            # The first span seem to always be the author
            author: str = author_div.find("span").text
            # print(author)
        except AttributeError:
            print("error finding the author")
            author = "Unknown author"

        try:
            full_date: str = author_div.find("time", "DateDisplay")["datetime"]
            date_obj: datetime = datetime.strptime(full_date, "%Y-%m-%dT%H:%M:%S.%fZ")
            # print(date_obj)
        except TypeError:
            print("error finding date\ninserting today's date instead")
            date_obj: datetime = datetime.now()

        try:
            full_article = soup.find_all("div", attrs={"class": "text_editor_paragraph rtl"})
            full_article_text: List[str] = [article.text for article in full_article]
            full_article_text: str = '\n\n'.join(full_article_text)
            # print(full_article_text)
        except TypeError:
            print("error getting article text")
            full_article_text: str = "Failed to get text"

        try:
            full_article = soup.find("div", {"data-contents": "true"})
            images_parent_div = full_article.find_all("a", {"class": "gelleryOpener"})
            images = [img.find("img")["src"] for img in images_parent_div]
            # print(images)
        except AttributeError:
            print("error getting images")
            images = []

        article = ArticleData(title=title, author=author, publication_date=date_obj, content=full_article_text, image_urls=images)
        articles_list.append(article)
        # print(article)
    return articles_list

urls = [
    "https://www.ynet.co.il/news/article/rkq6sbvkee",
    "https://www.ynet.co.il/news/article/rkrgxm9egx",
    "https://www.ynet.co.il/news/article/syot2cfxee",
    "https://www.ynet.co.il/news/article/s11f6etgxl",
]

print(scrape_ynet_articles(urls))
