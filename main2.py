import requests
from bs4 import BeautifulSoup
import lxml
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint
import os
from dotenv import load_dotenv

load_dotenv()



date=input("ENTER THE DATE IN YYYY-MM-DD Format:")
response = requests.get("https://www.billboard.com/charts/hot-100/" + date)
# print(response)
details=response.text
songs_detail=BeautifulSoup(details,'lxml')
song_=songs_detail.select("li ul li h3")
song_names=[s.getText().strip() for s in song_]
# print(song_names)






CLIENT_ID=os.environ.get("CLIENT_ID")
CLIENT_SCERETE=os.environ.get("CLIENT_SCERETE")


spo=spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SCERETE,
    redirect_uri="https://syncify.com/sync",
    scope="playlist-modify-private",
    show_dialog=True,
    cache_path="token2.txt",
    # username="Lingesh",

))

user_id=spo.current_user()["id"]
print(user_id)

song_uri=[]
year=date.split('-')[0]
for i in song_names:
    search=spo.search(q=f"track:{i} year:{year}",type="track")
    # pprint.pp(search)
    try:
        uri=search["tracks"]["items"][0]["uri"]
        song_uri.append(uri)
    except IndexError:
        print("NOT FOUND")


# print(song_uri)

playlist=spo.user_playlist_create(user=user_id,public=False,name=f"{date} SONGS")

print(playlist)
spo.playlist_add_items(playlist_id=playlist['id'],items=song_uri)



