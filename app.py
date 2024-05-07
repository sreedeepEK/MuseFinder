import streamlit as st 
import pickle 
import os 
import pandas as pd 
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

client_credentials_manager = SpotifyClientCredentials(client_id=os.getenv('client_id'), client_secret=os.getenv('client_secret'))
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def fetch_poster(track_name):
    track = sp.search(q=track_name, type="track", limit=1)
    if track['tracks']['items']:
        return track['tracks']['items'][0]['album']['images'][0]['url']
    else:
        return None

def recommend(selected_music):
    music_index = music[music['title']==selected_music].index[0]
    distance = similarity[music_index]
    music_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_music = []
    recommended_music_poster = []
    for i in music_list:
        music_title = music.iloc[i[0]].title
        recommended_music.append(music_title)
        poster_url = fetch_poster(music_title)
        if poster_url:
            recommended_music_poster.append(poster_url)
        else:
            recommended_music_poster.append("No poster found")
    return recommended_music, recommended_music_poster

music_dict = pickle.load(open('music.pkl','rb'))
music = pd.DataFrame(music_dict)

similarity = pickle.load(open('similarity.pkl','rb'))
st.title("Music Recommendation System")

selected_music_name = st.selectbox("Select a music you would like.", music['title'].values)

if st.button("Recommend"):
    names , posters = recommend(selected_music_name)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    for name, poster, col in zip(names, posters, [col1, col2, col3, col4, col5]):
        with col:
            st.text(name)
            st.image(poster)
