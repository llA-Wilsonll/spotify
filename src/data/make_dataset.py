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
tracks_dict = {}

keys = ['name', 'duration_ms', 'popularity']  # List of keys we want from the api response


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
    tracks_dict[country] = data["tracks"]

    # Taking a subset of the keys
    for i in range(len(tracks_dict[country])):
        tracks_dict[country][i] = extract(keys, tracks_dict[country][i])

    # Changing from list to DataFrame
    tracks_dict[country] = pd.DataFrame(tracks_dict[country])

# Concatenating dict of country DataFrames into one DataFrame
tracks_df = pd.concat(tracks_dict, sort=False)
tracks_df.reset_index(inplace=True)
tracks_df.columns = ['country', 'number'] + keys

# Inspecting to see if country data sets are actually different
cross_tab = pd.crosstab(tracks_df.name, tracks_df.number).apply(lambda r: r / r.sum(), axis=1)


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
