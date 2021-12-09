import json
import socket
from _thread import *

import DBTool

ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1232
ThreadCount = 0
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(10)

db = DBTool.DataBTool()
threads_game = list(list())
my_lock = RLock()


def get_information_movie(title) -> json:
    data = db.get_movie_info(title)
    print(data)
    return json.dumps(data)


def get_actors_movie(movie) -> json:
    data = db.get_movie_cast(movie)
    return json.dumps(data)


def get_information_actor(name) -> json:
    data = db.get_actor_movies(name)
    return json.dumps(data)


def get_reviews(movie) -> json:
    data = db.get_reviews(movie)
    return json.dumps(data)


def threaded_client(connection):
    connection.send(str.encode('Welcome to the Server'))
    while True:
        reply = ""
        data = connection.recv(2048)
        client_msg = data.decode('utf-8').split("-")
        if client_msg[0] == "movie":
            reply = get_information_movie(client_msg[1])
        if client_msg[0] == "actor":
            reply = get_information_actor(client_msg[1])
        if client_msg[0] == "movies":
            reply = get_actors_movie(client_msg[1])
        if client_msg[0] == "reviews":
            reply = get_reviews(client_msg[1])
        if client_msg[0] == "stop":
            break
        length_msg = len(reply)
        connection.sendall(str.encode(str(length_msg)))
        connection.sendall(str.encode(reply))
    connection.close()


while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client,))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSocket.close()
