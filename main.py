from bs4 import BeautifulSoup
import requests
from datetime import datetime
from pprint import pprint
import os
import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth


CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
URL_THE_KNOT = "https://www.theknot.com/content/best-love-songs"
# URL ="https://www.billboard.com/charts/hot-100/"
# date = input("What date would you like to travel back to [YYYY-MM-DD]!: ")
date = "2000-01-01"
# response = requests.get(f"{URL}{date}")

response = requests.get(url=URL_THE_KNOT)
website = response.text


soup = BeautifulSoup(website, "html.parser")
# print(soup.prettify())

# song_span = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
# singer_span = soup.find_all(name="span", class_="chart-element__information__artist text--truncate color--secondary")
# all_singers = [singer.getText() for singer in singer_span]
# all_songs = [song.getText() for song in song_span]
# print(all_songs)
song_tags = soup.find_all(name="strong")
all_songs = [song.getText().split("by")[0].replace('"', '').strip() for song in song_tags]
pprint(all_songs)
# sp = spotipy.Spotify(
#     auth_manager=SpotifyClientCredentials(
    # client_id = CLIENT_ID,
    # client_secret = CLIENT_SECRET,
#     ))
# search(q, limit=10, offset=0, type='track', market=None)
# results = sp.search(q='avant', type='track', )
# for idx, track in enumerate(results['tracks']['items']):
#     print(idx, track['name'])
#     print(f"audio    :  + {track['preview_url']}")
#     print(f"cover art:  + {track['album']['images'][0]['url']}")


sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
        ))
user_id = sp.current_user()["id"]
print(user_id)
songs_uri_list = []
year = date.split("-")[0]

# results = sp.current_user_saved_tracks()
for song in all_songs:
        result = sp.search(q=f"track:{song} year:{year}", type="track")
        # pprint(result)
        try:
                uri = result['tracks']["items"][0]["uri"]
                songs_uri_list.append(uri)
        except IndexError:
                print(f"spotify doesnt have that {song} ")

# pprint(songs_uri_list)
#Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
pprint(playlist)

#Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=songs_uri_list)