!pip install spotipy
!pip install streamlit
!pip install spotify-api


#for sharing playlist
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import spotifyAPI
import textwrap, random


# more imports for the spotify api
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
# api requests

##week 2(more imports)
import requests
import base64
import json

# received from the spotify developer account
client_id = '80d232eeaa064241b531967dfaccb515'
client_secret = '6b5084a5a9834bcb974bfb4d6c2a96d9'


os.environ["SPOTIPY_CLIENT_ID"] = client_id
os.environ["SPOTIPY_CLIENT_SECRET"] = client_secret
os.environ["SPOTIPY_REDIRECT_URI"] = "https://open.spotify.com/"
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())



sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='YOUR_CLIENT_ID',
                                               client_secret='YOUR_CLIENT_SECRET',
                                               redirect_uri='YOUR_REDIRECT_URI',
                                               scope='user-library-read'))

# song_name = ""  #insert song name    #need to integrate this part

# track_features = spotipy.audio_features(song_name)
# track_features
track = input("Song: ")  # need to figure out how to accept url in this
print(track)

#week 2

# urls that will be used to interact with the spotify api
SPOTIFY_API_TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_API_SEARCH_URL = 'https://api.spotify.com/v1/search'

# Authentication headers
# storing cause required for making authorized requests to the Spotify API
HEADERS = {}

# Function to obtain an access token from Spotify
def get_access_token():
    global HEADERS
    if 'access_token' not in HEADERS:
        # Create a Base64 encoded string with the client ID and client secret
        auth_str = f'{client_id}:{client_secret}'
        auth_b64 = base64.b64encode(auth_str.encode()).decode()
        headers = {
            'Authorization': f'Basic {auth_b64}',
        }
        data = {
            'grant_type': 'client_credentials',
        }
        # Request an access token from Spotify using client credentials
        response = requests.post(SPOTIFY_API_TOKEN_URL, headers=headers, data=data)
        access_token = json.loads(response.text)['access_token']
        HEADERS['Authorization'] = f'Bearer {access_token}'

print(HEADERS)
get_access_token()
print(HEADERS)

# 

df=pd.read_csv('Data/1mV3.csv')
artist_features=pd.read_csv('Data/artist_features.csv')
audio_features=pd.read_csv('Data/audio_features.csv')
track_features=pd.read_csv('Data/track_features.csv')

df = pd.merge(df,audio_features, left_on = "track_uri", right_on= "id",how = 'outer')
df = pd.merge(df,track_features, left_on = "track_uri", right_on= "Track_uri",how = 'outer')
df = pd.merge(df,artist_features, left_on = "artist_uri", right_on= "Artist_uri",how = 'outer')

#handling missing data
df.isna().sum()

missing_t_uri=df.track_uri[df.id.isna()]
missing_t_uri=missing_t_uri.unique()
random.shuffle(missing_t_uri)

f = open('data/audio_features.csv','a')
for i in tqdm(range(0,len(missing_t_uri),1)):
    try:
     track_feature = sp.audio_features(missing_t_uri[i:i+1])
     track_df = pd.DataFrame(track_feature)
     csv_data = track_df.to_csv(header=False,index=False)
     f.write(csv_data)
    except Exception as e:
        r = open("extract_log0.txt", "a")
        r.write(datetime.datetime.now().strftime("%d.%b %Y %H:%M:%S")+": "+str(e)+'\n')
        r.close()
        time.sleep(1)
        continue
f.close()

#cotd..
missing_t_uri=df.track_uri[df.Track_uri.isna()]
missing_t_uri=missing_t_uri.unique()
random.shuffle(missing_t_uri)

f = open('data/track_features.csv','a')
for i in tqdm(range(0,len(missing_t_uri),1)):
    try:
        track_features = sp.tracks(missing_t_uri[i:i+1])
        for x in range(1):
            track_pop=pd.DataFrame([missing_t_uri[i+x]])
            track_pop['release_date']=track_features['tracks'][x]['album']['release_date']
            track_pop['pop'] = track_features['tracks'][x]["popularity"]
            csv_data = track_pop.to_csv(header=False,index=False)
            f.write(csv_data)
    except Exception as e:
        r = open("extract_log.txt", "a")
        r.write(datetime.datetime.now().strftime("%d.%b %Y %H:%M:%S")+": "+str(e)+'\n')
        r.close()
        time.sleep(1)
        continue
f.close()

# removing unwanted data -- columns tio save space (help with pre poccessing)
df.dropna(axis=0,inplace=True)

df.isna().sum().sum()
df.columns
df.drop(columns=['Track_uri','Artist_uri','type','id','uri','track_href','analysis_url'],axis=1,inplace=True)
df.drop(columns=['Track_uri','Artist_uri','type','id','uri','track_href','analysis_url'],axis=1,inplace=True)
df.head(1)
# data pre processing process
df['Track_pop'] = df['Track_pop'].apply(lambda x: int(x/5))
df['Artist_pop'] = df['Artist_pop'].apply(lambda x: int(x/5))
df['Track_release_date'] = df['Track_release_date'].apply(lambda x: x.split('-')[0])
df['Track_release_date']=df['Track_release_date'].astype('int16')
df['Track_release_date'] = df['Track_release_date'].apply(lambda x: int(x/50))
df.to_csv('data/1M_unique_processed_data.csv',index=False)
