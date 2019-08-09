"""
The purpose of this code is to use the Spotify API to download the data 
I want to analyse. More specifically:
    - Download the top songs from the Beatles from numerous countries
    - Download an extensive list of The Beatles songs from a playlist
"""

import requests  # Used for API calls
from spfy_token import AccessToken  # Module where I store my access token
import pandas as pd  # DataFrame, concat, crosstab

# Instructions on how to obtain Auth Token can be found in docs directory
access_token = AccessToken.TOKEN

""" 
Downloading the Top songs from The Beatles 
"""

# You can search for Artist IDs using:
# https://developer.spotify.com/console/get-search-item/?q=AC%2FDC&type=artist&market=&limit=&offset=
# Artist ID for The Beatles
artist_id = "3WrFJ7ztbogyGnTHbHJFl2"

# URL Endpoint
url = "https://api.spotify.com/v1/artists/" + artist_id + "/top-tracks"

# Specfiying the countries we want the top songs of
countries = ["AU", "US", "GB", "CN", "JP", "BR", "DE", "ZA", "SE", "SG"]

# Initialising a dictionary to store track data for each country
top_tracks_dict = {}

keys = ['id', 'name', 'duration_ms', 'popularity']  # List of keys we want from the api response


# Function to extract subset of key-value pairs from a dict
def extract(x, y):
    return dict(zip(x, map(y.get, x)))


# Looping through each country and extracting the top 10 songs
for country in countries:
    # Parameters to URL Endpoint
    parameters = {"id": artist_id, "country": country}

    # Headers for URL Endpoint
    headers = {'Accept': 'application/json',
               'Content-Type': 'application/json',
               'Authorization': 'Bearer {0}'.format(access_token)}

    # Get the spotify data
    response = requests.get(url, params=parameters, headers=headers)
    # Print the status code of the response.
    # print('STATUS CODE: ' + str(response.status_code))

    data = response.json()
    top_tracks_dict[country] = data["tracks"]

    # Taking a subset of the keys
    for i in range(len(top_tracks_dict[country])):
        top_tracks_dict[country][i] = extract(keys, top_tracks_dict[country][i])

    # Changing values from list to DataFrame
    top_tracks_dict[country] = pd.DataFrame(top_tracks_dict[country])

# Concatenating dict of country DataFrames into one DataFrame
top_tracks_df = pd.concat(top_tracks_dict, sort=False)
top_tracks_df.reset_index(inplace=True)
top_tracks_df.columns = ['country', 'number'] + keys

# Inspecting to see if country data sets are actually different
cross_tab = pd.crosstab(top_tracks_df.name, top_tracks_df.number).apply(lambda r: r / r.sum(), axis=1)


""" 
Grab playlist of The Beatles songs 
"""

# Playlist id for "Beatles Greatest Hits"
playlist_id = "1FbXE0DKfcNlIRexSEHcs8"

# URL Endpoint
url = "https://api.spotify.com/v1/playlists/" + playlist_id + "/tracks"

# Specifying the fields to return
parameters = {'fields': 'items(track(id, name, duration_ms, popularity))'}

# Headers for URL Endpoint
headers = {'Accept': 'application/json',
           'Content-Type': 'application/json',
           'Authorization': 'Bearer {0}'.format(access_token)}

# Get the songs from the playlist
response = requests.get(url, params=parameters, headers=headers)

data = response.json()

for i in range(len(data['items'])):
    data['items'][i] = data['items'][i]['track']

playlist_tracks_df = pd.DataFrame(data['items'])
print(playlist_tracks_df)
print(playlist_tracks_df.columns)

"""
Getting Audio Features from the tracks in the playlist
"""

track_features_dict = {}

for track_id in playlist_tracks_df["id"]:

    # URL Endpoint
    url = "https://api.spotify.com/v1/audio-features/" + track_id

    # Headers for URL Endpoint
    headers = {'Accept': 'application/json',
               'Content-Type': 'application/json',
               'Authorization': 'Bearer {0}'.format(access_token)}

    # Get the songs from the playlist
    response = requests.get(url, headers=headers)

    data = response.json()

    # Storing response (form of simple dictionary) in the track_features_dict with key=track_id
    track_features_dict[track_id] = data

# Creating a pandas dataframe from the dictionary of dictionaries
track_features_df = pd.DataFrame.transpose(pd.DataFrame(track_features_dict))

# Resetting the index so the id becomes a column
track_features_df.reset_index(inplace=True)

# Renaming the index column back to id
track_features_df = track_features_df.rename(columns = {'index':'id'})

print(track_features_df)
print(track_features_df.columns)


"""
Pickle the Pandas DataFrames we want to save
    - Saving to the /data/raw subdirectory
"""

# Top tracks
top_tracks_df.to_pickle("../../data/raw/top_tracks.pkl")

# Tracks from the playlist
playlist_tracks_df.to_pickle("../../data/raw/playlist_tracks.pkl")

# Track Features
track_features_df.to_pickle("../../data/raw/track_features.pkl")
