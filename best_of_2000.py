from bs4 import BeautifulSoup
import requests
from datetime import datetime
from pprint import pprint

URI = "https://www.theknot.com/content/best-love-songs"


response = requests.get(url=URI)
web_data = response.text

soup = BeautifulSoup(web_data, "html.parser")
song_tags = soup.find_all(name="strong")
songs = [song.getText().split("by")[0].replace('"', '').strip() for song in song_tags]
pprint(songs)















