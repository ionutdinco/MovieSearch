import json
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

    def get_info(self, href, title) -> dict:
        results = dict()
        url = "https://www.imdb.com" + href
        self.page = requests.get(url)
        soup = BeautifulSoup(self.page.content, "lxml")
        print(title)
        results["title"] = title

        rating = soup.find("span", class_="AggregateRatingButton__RatingScore-sc-1ll29m0-1 iTLWoV").get_text()
        print(rating)
        results["rating"] = rating

        director = soup.find("a",
                             class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link").get_text()
        print(director)
        results["director"] = director

        image = soup.find("a", class_="ipc-lockup-overlay ipc-focusable")
        results["image"] = "https://www.imdb.com" + image.get("href")
        print(results["image"])

        reviews_url = url + "reviews/"
        page = requests.get(reviews_url)
        soup = BeautifulSoup(page.content, "lxml")
        reviews = soup.find_all("div", class_="text")
        i = 1
        rev = list()
        for review in reviews:
            if len(review.get_text()) < 2000:
                rev.append(review.get_text())
            if i == 7:
                break
            i += 1
        results["reviews"] = rev

        cast_url = url + "fullcredits/"
        page = requests.get(cast_url)
        soup = BeautifulSoup(page.content, "lxml")
        table = soup.find('table', class_="cast_list")
        cast = list()
        i = 1
        rows = table.find_all("td", class_="primary_photo")
        for row in rows:
            cast.append(row.find_next_sibling("td").text)
            if i == 10:
                break
            i += 1
        results["cast"] = cast

        trailer_url = "https://www.youtube.com/results?search_query=" + unicode(title + " movie trailer")
        page = requests.get(trailer_url)
        soup = page.text
        soup = soup[soup.find("navigationEndpoint"):]
        soup = soup[1:]
        soup = soup[soup.find("navigationEndpoint"):]
        soup = soup[soup.find("url"):soup.find("webPageType")]
        soup = soup[soup.find(':"') + 2:]
        soup = soup[:soup.find('"')]
        trailer = "https://www.youtube.com/" + soup
        results["trailer"] = trailer
        print(trailer)

        return results


if __name__ == '__main__':
    s = ScrapingTool()
    s.scrape_html_content("pirates of the caribbean: the curse of the black pearl")
