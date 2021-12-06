import json
import math

from tkinter import *
import socket
import random

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1232

try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))
response = ClientSocket.recv(1024).decode('utf-8')
print(response)


def send_msg_to_server(x):
    ClientSocket.sendall(str.encode(x))
    output = ClientSocket.recv(2048).decode('utf-8')
    return output


class ClientGraphics(object):
    W = 1500
    H = 700

    def __init__(self):
        self.nr_of_movies = 9
        self.reviews_rows = 5
        self.window = Tk()
        self.frame = Frame(self.window, bg='ghost white')
        self.window.geometry("1500x700")
        self.frame.pack(side="top", expand=True, fill="both")
        self.widgets = dict()
        self.movie = StringVar(self.frame)
        self.actor = StringVar(self.frame)
        self.lst = list()
        self.movies = list()
        self.total_rows = 4
        self.total_columns = 2
        self.home()

    def clear_frame(self):
        for widgets in self.frame.winfo_children():
            widgets.destroy()

    def search_for_movie(self):
        self.clear_frame()
        width = 400
        height = 100
        x = self.W / 2 - width / 2
        y = self.H / 2 - height / 2
        entry_movie = Entry(self.frame, textvariable=self.movie, bg='snow', font=('Arial', 20, 'bold'))
        entry_movie.place(x=self.W / 2 - width / 2, y=self.H / 2 - 1.5 * height, width=width, height=height)
        self.widgets["entry_movie"] = entry_movie
        button_movie = Button(self.frame, text="Search For Movie", command=self.get_movie, bg='snow')
        button_movie.place(x=self.W / 2 - width / 2, y=self.H / 2 + 0.5 * height, width=width, height=height)
        button_back = Button(self.frame, text="< Go Back", command=self.home, bg='snow')
        button_back.place(x=self.W / 4 - width / 2, y=self.H - self.H / 4 + 0.5 * height, width=width, height=height)

    def search_for_actor(self):
        self.clear_frame()
        width = 400
        height = 100
        x = self.W / 2 - width / 2
        y = self.H / 2 - height / 2
        entry_actor = Entry(self.frame, textvariable=self.actor, bg='snow', font=('Arial', 20, 'bold'))
        entry_actor.place(x=self.W / 2 - width / 2, y=self.H / 2 - 1.5 * height, width=width, height=height)
        self.widgets["entry_actor"] = entry_actor
        button_actor = Button(self.frame, text="Search For Actor", command=self.get_movie_actors, bg='snow')
        button_actor.place(x=self.W / 2 - width / 2, y=self.H / 2 + 0.5 * height, width=width, height=height)
        button_back = Button(self.frame, text="< Go Back", command=self.home, bg='snow')
        button_back.place(x=self.W / 4 - width / 2, y=self.H - self.H / 4 + 0.5 * height, width=width, height=height)

    def home(self):
        self.clear_frame()
        width = 400
        height = 100
        button_movie = Button(self.frame, text="Search For Movie", command=self.search_for_movie, bg='snow')
        button_movie.place(x=self.W / 2 - 1.5 * width, y=self.H / 2 - height / 2, width=width, height=height)
        button_actor = Button(self.frame, text="Search For Actor", command=self.search_for_actor, bg='snow')
        button_actor.place(x=self.W / 2 + 0.5 * width, y=self.H / 2 - height / 2, width=width, height=height)

    def display_info_movie(self):
        self.clear_frame()
        width = 400
        height = 100
        canvas = Canvas(self.frame, width=400, height=100, bg='white')
        canvas.pack()
        for i in range(self.total_rows):
            for j in range(self.total_columns):
                if j % 2 == 1:
                    cell = Text(canvas, width=50, height=5, fg='blue',
                                font=('Arial', 16, 'bold'), borderwidth=4, relief="groove")
                    cell.grid(row=i, column=j)
                    cell.insert(END, self.lst[i][j])
                else:
                    cell = Text(canvas, width=20, height=5, fg='blue',
                                font=('Arial', 16, 'bold'), borderwidth=4, relief="groove")
                    cell.grid(row=i, column=j)
                    cell.insert(END, self.lst[i][j])
        button_reviews = Button(self.frame, text="Reviews >", command=self.display_reviews, bg='snow')
        button_reviews.place(x=self.W / 2 + 0.5 * width, y=self.H - 1.5 * height, width=width, height=height)
        button_back = Button(self.frame, text="< Go Back", command=self.search_for_movie, bg='snow')
        button_back.place(x=self.W / 4 - width / 2, y=self.H - 1.5 * height, width=width, height=height)

    def display_info_actor(self):
        self.clear_frame()
        width = 400
        height = 100
        canvas = Canvas(self.frame, width=400, height=100, bg='white')
        canvas.pack()
        for i in range(len(self.movies) - 1):
            cell = Label(canvas, width=50, height=2, fg='blue', text=self.movies.pop(0),
                        font=('Arial', 16, 'bold'), relief="groove")
            cell.pack()
        button_back = Button(self.frame, text="< Go Back", command=self.search_for_actor, bg='snow')
        button_back.place(x=self.W / 4 - width / 2, y=self.H - 1.5 * height, width=width, height=height)



if __name__ == '__main__':
    w = ClientGraphics()
    w.window.mainloop()
# x = send_msg_to_server("movie:PIRATHES pf the C 2")
# print(x)
