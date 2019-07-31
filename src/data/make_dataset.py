"""
The purpose of this code is to use the Spotify API to download the data 
I want to analyse. More specifically:
    - Download the top songs from the Beatles from numerous countries
    - Download an extensive list of The Beatles songs from a playlist
"""

import requests # Used for API calls
import json # To parse response from API call
from spfy_token import AccessToken # Module where I store my access token

# Instructions on how to obtain Auth Token can be found in docs directory
access_token = AccessToken.TOKEN

# You can search for Artist IDs using: https://developer.spotify.com/console/get-search-item/?q=AC%2FDC&type=artist&market=&limit=&offset=
# Artist ID for The Beatles
artist_id = "3WrFJ7ztbogyGnTHbHJFl2"

# URL Endpoint
url = "https://api.spotify.com/v1/artists/" + artist_id + "/top-tracks"

# Specfiying the countries we want the top songs of
countries = ["AU","US","GB","CN","JP","BR","DE","ZA","SE","SG"]

# Initialising a dictionary to store track data for each country
tracks = {}

# Looping through each country and extracting the top 10 songs
for country in countries:
   # Paramters to URL Endpoint
   parameters = {"id": artist_id, "country": country}

   # Headers for URL Endpoint
   headers = {'Accept': 'application/json',
           'Content-Type': 'application/json',
           'Authorization': 'Bearer {0}'.format(access_token)}

   # Get the spotify data
   response = requests.get(url, params=parameters, headers=headers)
   # Print the status code of the response.
   print('STATUS CODE: ' + str(response.status_code))

   data = response.json()
   tracks[country] = data["tracks"]
   print('Number of countries: ' + str(len(tracks)))