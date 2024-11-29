import requests
from bs4 import BeautifulSoup
import lxml
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()




CLIENT_ID=os.environ.get("CLIENT_ID")
CLIENT_SCERETE=os.environ.get("CLIENT_SCERETE")
URI=os.environ.get("URI")
USER_ID=os.environ.get("USER_ID")


year="2010-08-12"#input("Which year would you Like to Travel?")
billboard="https://www.billboard.com/charts/hot-100/"+year

response=requests.get(url=billboard)
print(response)
html=response.text
soup=BeautifulSoup(html,"lxml")

# s=soup.find_all(name="h3",id="title-of-a-story")
s=soup.select("li ul li h3")
songs=[sng.getText().strip() for sng in s]
# print(songs)


sop=spotipy.SpotifyOAuth(client_id=CLIENT_ID,client_secret=CLIENT_ID,redirect_uri=URI)
print(sop)



sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=URI,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SCERETE,
        show_dialog=True,
        cache_path="token.txt",
        # username="LINGESH.R", 
    )
)
user_id = sp.current_user()["id"]
date="2010-08-12"#input("Which year would you Like to Travel?")
split_date=date.split('-')[0]

song_uris=[]
for sgs in songs:
    result=sp.search(q=f"track:{sgs} year:{split_date}",type="track")
    print(result)

    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{sgs} doesn't exist in Spotify. Skipped.")


playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)


