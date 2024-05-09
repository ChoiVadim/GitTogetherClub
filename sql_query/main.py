import time
import random
import sqlite3
import tkinter as tk
from tkinter import messagebox

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class MyGUI:
    def __init__(self):
        self.random_movie = ""

        self.root = tk.Tk()
        self.root.title("Random Movie Generator")
        self.root.minsize(width=400, height=300)
        self.root.config(bg="black")

        label_font = ("Roboto", 12, "bold")
        button_font = ("Roboto", 10)
        main_label_font = ("Roboto", 18, "bold")

        label = tk.Label(self.root, text="Enter rating:", bg="black", font=label_font)
        label.config(fg="white")
        label.pack(padx=10, pady=5)

        self.textbox_rating = tk.Text(self.root, width=5, height=1, font=("Arial", 14))
        self.textbox_rating.pack(padx=10, ipadx=5)

        label2 = tk.Label(self.root, text="Enter genre:", bg="black", font=label_font)
        label2.config(fg="white")
        label2.pack(padx=10, pady=5)

        self.textbox_genre = tk.Text(self.root, width=10, height=1, font=("Arial", 14))
        self.textbox_genre.pack(padx=10, ipadx=5)
        self.textbox_genre.bind("<KeyPress>", self.shortcut)

        self.label = tk.Label(
            self.root, text="Random Movie Searcher", font=main_label_font, bg="black"
        )
        self.label.config(fg="white")
        self.label.pack(padx=10, pady=(10, 20), ipady=5)

        self.get_movie_btn = tk.Button(
            self.root,
            text="Random",
            font=button_font,
            command=self.get_random_movie,
            bg="blue",
        )
        self.get_movie_btn.config(fg="white")
        self.get_movie_btn.pack(ipadx=15, ipady=7)

        self.search_btn = tk.Button(
            self.root,
            text="Trailer",
            font=button_font,
            command=self.search_youtube,
            bg="green",
            fg="white",
        )
        self.search_btn.config(fg="white")
        self.search_btn.pack(ipadx=20, pady=10, ipady=7)

        self.root.mainloop()

    def shortcut(self, event):
        if event.keysym == "Return" and event.state == 0:
            print("Enter pressed")

    def get_rating_and_genre(self):
        rating = self.textbox_rating.get("1.0", "end").strip()
        genre = self.textbox_genre.get("1.0", "end").strip().capitalize()
        return rating, genre

    def get_random_movie(self):
        results = self.get_movies_from_db()
        print(f"{len(results)} movies found")

        self.random_movie = random.choice(results)
        print(self.random_movie)

        self.label.config(text=f"{self.random_movie[0]} ({self.random_movie[1]})")

        return self.random_movie

    def get_movies_from_db(self):
        rating, genre = self.get_rating_and_genre()

        query = f"""
            SELECT t.primary_title, t.premiered, r.rating, r.votes
            FROM titles t JOIN ratings r
            ON t.title_id = r.title_id 
            WHERE r.rating >= {rating}
            AND t.genres LIKE "%{genre}%"
            AND r.votes >= 1000
            AND t.premiered >= 2000;
        """

        conn = sqlite3.connect("imdb.db")
        c = conn.cursor()
        c.execute(query)
        results = c.fetchall()

        return results

    def search_youtube(self):
        driver = webdriver.Chrome()  # webdriver.Chrome('/path/to/chromedriver')

        driver.get("https://www.youtube.com")
        time.sleep(3)

        search_box = driver.find_element(By.NAME, "search_query")

        search_box.send_keys(f"Trailer {self.random_movie[0]} ({self.random_movie[1]})")
        search_box.send_keys(Keys.RETURN)

        time.sleep(4)

        try:
            videos = driver.find_elements(By.ID, "video-title")
            if len(videos) >= 2:
                second_video = videos[1]
                second_video.click()
            else:
                print("Not enough videos found.")
        except Exception as e:
            messagebox.showinfo("Error", "Cant find trailer!")

        while True:
            if messagebox.askyesno("Trailer was found", "Do you want to close?"):
                break

        driver.quit()


if __name__ == "__main__":
    MyGUI()
