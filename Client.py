from io import BytesIO
import json
from tkinter import *
from tkinter import messagebox

from PIL import Image, ImageTk
import urllib.request
import socket
import webbrowser

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
    size = ClientSocket.recv(1024).decode('utf-8')
    output = ClientSocket.recv(int(size)).decode('utf-8')
    return output


class ClientGraphics(object):
    W = 1500
    H = 700

    def __init__(self):
        self.window = Tk()
        self.frame = Frame(self.window, bg='peach puff')
        self.window.geometry("1500x700")
        self.window.title("SearchMovieTool")
        self.frame.pack(side="top", expand=True, fill="both")
        self.widgets = dict()
        self.pos = 0
        self.movie = ""
        self.actor = ""
        self.url_image = ""
        self.trailer = ""
        self.search = StringVar(self.frame)
        self.search_type = StringVar(self.frame)
        self.lst = list()
        self.movies = list()
        self.reviews = list()
        self.total_rows = 5
        self.total_columns = 2
        self.w = 300
        self.h = 50
        self.home()

    def clear_frame(self):
        for widgets in self.frame.winfo_children():
            widgets.destroy()

    def select(self):
        print(self.search_type.get())
        pass

    def home(self):
        self.clear_frame()
        entry_movie = Entry(self.frame, textvariable=self.search, bg='snow', font=('Arial', 15, 'bold'))
        entry_movie.place(x=self.W / 2 - 3 / 4 * self.w, y=self.H / 2 - 1.5 * self.h, width=3 / 2 * self.w,
                          height=self.h)
        self.search_type.set("Movie")
        radio_btn1 = Radiobutton(self.frame, text="Movie", variable=self.search_type, value="Movie", bg="peach puff",
                                 command=self.select)
        radio_btn1.place(x=self.W / 2 - self.w / 2, y=self.H / 2 + 0.1 * self.h)

        radio_btn2 = Radiobutton(self.frame, text="Actor", variable=self.search_type, value="Actor", bg="peach puff",
                                 command=self.select)
        radio_btn2.place(x=self.W / 2 + self.w / 2, y=self.H / 2 + 0.1 * self.h)
        button_movie = Button(self.frame, text="Search", command=self.parse_input, bg='steel blue')
        button_movie.place(x=self.W / 2 - self.w / 2, y=self.H / 2 + 0.5 * self.h, width=self.w, height=self.h)

    def parse_input(self):
        if self.search_type.get() == "Movie":
            self.movie = self.search.get()
            self.get_movie()
        if self.search_type.get() == "Actor":
            self.actor = self.search.get()
            self.get_movie_actors()

    def display_info_movie(self):
        self.clear_frame()
        link_window = None
        canvas = Canvas(self.frame, bg='peach puff')
        canvas.pack()
        for i in range(self.total_rows):
            for j in range(self.total_columns):
                if j % 2 == 1:
                    if i == 4:
                        cell = Text(canvas, width=50, height=6, fg='white', bg="steel blue", padx=5, pady=5,
                                    font=('Columbo', 16, 'bold'), borderwidth=4, relief="groove")
                        cell.grid(row=i, column=j)
                        cell.insert(END, self.lst[i][j])
                        cell.config(state=DISABLED)
                        scrollbar = Scrollbar(canvas, orient='vertical', command=cell.yview)
                        scrollbar.grid(row=i, column=2, sticky='ns')
                        cell['yscrollcommand'] = scrollbar.set
                    else:
                        cell = Text(canvas, width=50, height=3, fg='white', bg="steel blue", padx=5, pady=5,
                                    font=('Royal Acid', 16, 'bold'), borderwidth=4, relief="groove")
                        cell.grid(row=i, column=j)
                        cell.insert(END, self.lst[i][j])
                        cell.config(state=DISABLED)
                        if i == 1:
                            link_window = cell
                else:
                    if i == 4:
                        cell = Text(canvas, width=20, height=6, fg='white', bg="steel blue", padx=5, pady=5,
                                    font=('Columbo', 16, 'bold'), borderwidth=4, relief="groove")
                        cell.grid(row=i, column=j)
                        cell.insert(END, self.lst[i][j])
                        cell.config(state=DISABLED)
                    else:
                        cell = Text(canvas, width=20, height=3, fg='white', bg="steel blue", padx=5, pady=5,
                                    font=('Columbo', 16, 'bold'), borderwidth=4, relief="groove")
                        cell.grid(row=i, column=j)
                        cell.insert(END, self.lst[i][j])
                        cell.config(state=DISABLED)

        link_window.bind("<Button-1>", self.open_url)

        button_reviews = Button(self.frame, text="Reviews >", command=self.display_reviews, bg='steel blue')
        button_reviews.place(x=self.W / 2 + 0.5 * self.w, y=self.H - 1.5 * self.h, width=self.w, height=self.h)
        button_reviews = Button(self.frame, text="< Back", command=self.home, bg='steel blue')
        button_reviews.place(x=self.W / 2 - 0.5 * self.w, y=self.H - 1.5 * self.h, width=self.w, height=self.h)

        print(self.url_image)
        # with urllib.request.urlopen("http://www.python.org") as url:
        #     raw_data = url.read()
        # url.close()
        # im = Image.open(BytesIO(raw_data))
        # image = ImageTk.PhotoImage(im)
        # label1 = Label(self.frame, image=image)
        # label1.place(x=0, y=0)

    def display_info_actor(self):
        self.clear_frame()
        canvas = Canvas(self.frame, width=400, height=100, bg='white')
        canvas.pack()
        for i in range(len(self.movies)):
            cell = Label(canvas, width=50, height=2, fg='blue', text=self.movies.pop(0),
                         font=('Arial', 16, 'bold'), relief="groove")
            cell.pack()
            cell.config(state=DISABLED)
        button_back = Button(self.frame, text="< Back", command=self.home, bg='steel blue')
        button_back.place(x=self.W / 4 - self.w / 2, y=self.H - 1.5 * self.h, width=self.w, height=self.h)

    def display_reviews(self):
        self.clear_frame()
        canvas = Canvas(self.frame, width=1500, height=600, bg='steel blue')
        cell = Text(canvas, fg='steel blue', font=('Courier', 16), borderwidth=4, relief="groove", padx=30, pady=30,
                    highlightbackground="SteelBlue4", highlightthickness=2, wrap=WORD, spacing2=2)
        cell.place(x=self.W / 4, y=50, width=2 * (self.W / 4), height=500)
        try:
            cell.insert(END, self.reviews[0])
        except IndexError:
            cell.insert(END, "doesn't have reviews")
        cell.config(state=DISABLED)
        self.widgets["cell"] = cell
        next_btn = canvas.create_polygon(self.W / 5, self.H / 2, self.W / 5 + 40, self.H / 2 - 40, self.W / 5 + 40,
                                         self.H / 2 + 40, self.W / 5, self.H / 2, fill="SteelBlue4", outline="white", width=2)
        prev_btn = canvas.create_polygon(4 * self.W / 5, self.H / 2, 4 * self.W / 5 - 40, self.H / 2 - 40,
                                         4 * self.W / 5 - 40, self.H / 2 + 40, 4 * self.W / 5, self.H / 2, fill="SteelBlue4",
                                         outline="white", width=2)
        canvas.tag_bind(next_btn, '<Button-1>', self.next)
        canvas.tag_bind(prev_btn, '<Button-1>', self.prev)
        canvas.pack()

        button_back = Button(self.frame, text="< Back", command=self.display_info_movie, bg='steel blue')
        button_back.place(x=self.W / 4 - self.w / 2, y=self.H - 1.5 * self.h, width=self.w, height=self.h)

    def get_movie(self):
        if len(self.movie) > 0:
            self.lst.clear()
            client_msg = "movie-" + self.movie
            movie_info = None
            try:
                movie_info = json.loads(send_msg_to_server(client_msg))
                keys = list(movie_info.keys())
                for i in range(self.total_rows - 1):
                    tp = (keys[i], movie_info.get(keys[i]))
                    self.lst.append(tp)
                self.url_image = movie_info.get("movieImage")
                self.trailer = movie_info.get("movieTrailer")

                client_msg = "movies-" + self.movie
                serv_info = json.loads(send_msg_to_server(client_msg))
                actors = "\n".join(serv_info["cast"])
                tp = ("Actors", actors)
                self.lst.append(tp)

                client_msg = "reviews-" + self.movie
                serv_info = json.loads(send_msg_to_server(client_msg))
                self.reviews = serv_info["reviews"]

                self.display_info_movie()

            except ValueError:
                messagebox.showerror('BAD LUCK', 'Movie Not Found! Try Again!')

    def get_movie_actors(self):
        if len(self.actor) > 0:
            client_msg = "actor-" + self.actor
            serv_info = json.loads(send_msg_to_server(client_msg))
            self.movies = serv_info["movies"]
            print(self.movies)
            self.display_info_actor()

    def next(self, event):
        self.widgets["cell"].config(state=NORMAL)
        self.widgets["cell"].delete('1.0', END)
        if self.pos == len(self.reviews) - 1:
            self.pos = 0
        else:
            self.pos += 1
        try:
            self.widgets["cell"].insert(END, self.reviews[self.pos])
        except IndexError:
            self.widgets["cell"].insert(END, "doesn't have reviews")
        self.widgets["cell"].config(state=DISABLED)

    def prev(self, event):
        self.widgets["cell"].config(state=NORMAL)
        self.widgets["cell"].delete('1.0', END)
        if self.pos == 0:
            self.pos = len(self.reviews) - 1
        else:
            self.pos -= 1
        try:
            self.widgets["cell"].insert(END, self.reviews[self.pos])
        except IndexError:
            self.widgets["cell"].insert(END, "doesn't have reviews")
        self.widgets["cell"].config(state=DISABLED)

    def open_url(self, event):
        webbrowser.open_new(self.trailer)


if __name__ == '__main__':
    w = ClientGraphics()
    w.window.mainloop()
