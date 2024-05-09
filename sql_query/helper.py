import time
import sqlite3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def search_youtube(movie_title):
    driver = webdriver.Chrome()  # webdriver.Chrome('/path/to/chromedriver')

    driver.get("https://www.youtube.com")
    time.sleep(3)

    search_box = driver.find_element(By.NAME, "search_query")

    search_box.send_keys(movie_title)
    search_box.send_keys(Keys.RETURN)

    time.sleep(3)

    videos = driver.find_elements(By.ID, "video-title")
    if len(videos) >= 2:
        second_video = videos[1]
        second_video.click()
    else:
        print("Недостаточно видео в результатах поиска.")

    input("Press any key to close...")
    driver.quit()


def get_movies(query):
    conn = sqlite3.connect("imdb.db")
    c = conn.cursor()
    c.execute(query)
    results = c.fetchall()
    return results
