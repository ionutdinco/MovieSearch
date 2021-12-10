import requests
from bs4 import BeautifulSoup
from numpy import unicode


class ScrapingTool(object):

    def __init__(self):
        self.baseURL = "https://www.imdb.com/find?q="
        self.page = None
        self.found = False

    def scrape_html_content(self, title_movie):
        words = unicode(title_movie)
        url = "https://www.imdb.com/find?q=" + words + "&s=tt&ttype=ft&exact=true"
        self.page = requests.get(url)
        soup = BeautifulSoup(self.page.content, "lxml")
        title = soup.find("td", class_="result_text")
        name = ""
        href = ""
        results = dict()

        if title:
            if "aka" in title.text:
                name = title.text.split("\"")[1]
            else:
                name = title.find("a").text
            if name.lower() == title_movie.lower():
                href = title.find("a").get("href")
                print(href)
                self.found = True
        if self.found:
            results = self.get_info(href, name)
        else:
            return None
        self.found = False
        return results

    def get_info(self, href, name):
        
        pass
