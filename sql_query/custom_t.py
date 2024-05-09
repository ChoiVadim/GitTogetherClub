import time
import random
import sqlite3
from tkinter import messagebox
from threading import Thread

import customtkinter
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("Dark")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("blue")


class MyGUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.random_movie = ""

        # Set the window title and size
        self.title("Random Movie Generator")
        self.minsize(width=400, height=300)

        # Create a frame
        frame = customtkinter.CTkFrame(master=self)
        frame.pack(pady=20, padx=60, fill="both", expand=True)

        # Initialize fonts
        label_font = customtkinter.CTkFont(size=16, weight="bold")
        button_font = customtkinter.CTkFont(size=16, weight="bold")
        main_label_font = customtkinter.CTkFont(size=20, weight="bold")

        # Create text box for rating
        self.textbox_rating = customtkinter.CTkEntry(
            master=frame,
            placeholder_text="Enter rating",
            width=100,
            height=2,
            font=label_font,
        )
        self.textbox_rating.pack(padx=10, pady=20)

        # Create text box for genre
        self.textbox_genre = customtkinter.CTkEntry(
            master=frame,
            placeholder_text="Enter genre",
            width=100,
            height=1,
            font=label_font,
        )
        self.textbox_genre.pack(padx=10)
        # Bind the Enter key to the shortcut function
        self.textbox_genre.bind("<KeyPress>", self.shortcut)

        # Create a main label for a movie title
        self.label = customtkinter.CTkLabel(
            master=frame, text="Random Movie Searcher", font=main_label_font
        )
        self.label.pack(padx=10, pady=(20, 20), ipady=5)

        # Create a button to get a random movie
        self.get_movie_btn = customtkinter.CTkButton(
            master=frame,
            text="Random",
            font=button_font,
            command=self.get_random_movie,
        )
        self.get_movie_btn.pack(pady=10)

        # Create a button to search for a trailer
        self.search_btn = customtkinter.CTkButton(
            master=frame,
            text="Trailer",
            font=button_font,
            command=lambda: Thread(target=self.search_youtube).start(),
        )
        self.search_btn.pack()

        # Start the main loop
        self.mainloop()

    def shortcut(self, event):
        # Check if the Enter key was pressed
        if event.keysym == "Return" and event.state == 0:
            print("Enter pressed")

    def get_rating_and_genre(self):
        # Get the rating and genre from the text boxes
        rating = self.textbox_rating.get().strip()
        genre = self.textbox_genre.get().strip().capitalize()
        return rating, genre

    def get_random_movie(self):
        results = self.get_movies_from_db()
        print(f"{len(results)} movies found")

        # Select a random movie
        self.random_movie = random.choice(results)
        print(self.random_movie)

        # Update the label
        self.label.configure(text=f"{self.random_movie[0]} ({self.random_movie[1]})")

        return self.random_movie

    def get_movies_from_db(self):
        # Return a list of movies from the database
        rating, genre = self.get_rating_and_genre()

        # Change this query to your needs
        query = f"""
            SELECT t.primary_title, t.premiered, r.rating, r.votes
            FROM titles t JOIN ratings r
            ON t.title_id = r.title_id 
            WHERE r.rating >= {rating}
            AND t.genres LIKE "%{genre}%"
            AND r.votes >= 1000
            AND t.premiered >= 2000;
        """

        # Connect to the database
        conn = sqlite3.connect("imdb.db")
        # Create a cursor
        c = conn.cursor()
        # Execute the query
        c.execute(query)
        # Fetch all the results
        results = c.fetchall()

        return results

    def search_youtube(self):
        # Initialize the web driver
        driver = webdriver.Chrome()  # webdriver.Chrome('/path/to/chromedriver')

        # Navigate to the YouTube website
        driver.get("https://www.youtube.com")
        time.sleep(3)

        # Find the search box and search for the trailer
        search_box = driver.find_element(By.NAME, "search_query")
        search_box.send_keys(f"Trailer {self.random_movie[0]} ({self.random_movie[1]})")
        search_box.send_keys(Keys.RETURN)
        time.sleep(4)

        try:
            # Find the second video and click it
            videos = driver.find_elements(By.ID, "video-title")
            if len(videos) > 1:
                second_video = videos[1]
                second_video.click()
            else:
                print("Not enough videos found.")

        except Exception as e:
            tkinter.messagebox.showinfo("Error", "Cant find trailer!")
            print(e)

        # Wait for the user to press "Yes" or "No"
        input_yes_no = False
        while not input_yes_no:
            input_yes_no = messagebox.askyesno(
                "Trailer was found", "Do you want to close?"
            )

        # Close the web driver
        driver.quit()


if __name__ == "__main__":
    MyGUI()
