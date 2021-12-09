import json

import mysql.connector
import numpy as np
from numpy import ndarray

import IMDBCrawl


class DataBTool(object):
    def __init__(self):
        self.data_base_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        self.cursor = self.data_base_connection.cursor()
        self.add_db()
        self.data_base = "movie_py"
        self.my_crawler = IMDBCrawl.ScrapingTool()

    def add_db(self):
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS movie_py")
        self.cursor.execute("USE movie_py")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS `movies_store` ("
                            "`idmovies` int(11) NOT NULL AUTO_INCREMENT,"
                            "`movieName` varchar(255) NOT NULL UNIQUE,"
                            "`movieTrailer` varchar(255) NOT NULL,"
                            "`movieDirector` varchar(255) NOT NULL,"
                            "`movieRating` double NOT NULL,"
                            "`movieImage` varchar(255) NOT NULL,"
                            "PRIMARY KEY (`idmovies`))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS `actors` ("
                            "`idActors` int(11) NOT NULL AUTO_INCREMENT,"
                            "`actorName` varchar(255) NOT NULL,"
                            "`movie` varchar(255) NOT NULL,"
                            "PRIMARY KEY (`idActors`))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS `reviews` ("
                            "`id` int(11) NOT NULL AUTO_INCREMENT,"
                            "`movieName` varchar(255) NOT NULL,"
                            "`comment` varchar(2000) NOT NULL,"
                            "PRIMARY KEY (`id`))")

    def get_movie_info(self, title):
        data = dict()
        self.cursor.execute("Select movieName, movieTrailer, movieRating, movieDirector, movieImage from movies_store where lower(movieName) = %s",
                            (title.lower().strip(),))
        result = self.cursor.fetchone()
        if result:
            for i in range(0, 5):
                data[self.cursor.description[i][0]] = result[i]
            self.data_base_connection.commit()
        else:
            print("online search for movie:", title)
            online_info = self.my_crawler.scrape_html_content(title)
            if online_info:
                self.insert_info_movie(online_info)
                data["movieName"] = online_info["title"].strip()
                data["movieTrailer"] = online_info["trailer"]
                data["movieRating"] = online_info["rating"]
                data["movieDirector"] = online_info["director"]
                data["movieImage"] = online_info["image"]
            else:
                return None
        print(len(json.dumps(data)))
        return data

    def get_actor_movies(self, name):
        data = dict()
        movies = []
        self.cursor.execute("Select movie from actors where lower(actorName) = %s", (name.lower(),))
        result = self.cursor.fetchall()
        for movie in result:
            movies.append(movie[0])
        data["movies"] = movies
        print(data)
        return data

    def get_movie_cast(self, movie):
        data = dict()
        cast = []
        self.cursor.execute("Select actorName from actors where lower(movie) = %s", (movie.lower(),))
        result = self.cursor.fetchall()
        for actor in result:
            cast.append(actor[0])
        data["cast"] = cast
        print(data["cast"])
        return data

    def get_reviews(self, movie):
        data = dict()
        reviews = []
        self.cursor.execute("Select comment from reviews where lower(movieName) = %s", (movie.lower(),))
        result = self.cursor.fetchall()
        for comment in result:
            reviews.append(comment[0])
        data["reviews"] = reviews
        print(data)
        return data

    def insert_info_movie(self, online_info):
        pass
