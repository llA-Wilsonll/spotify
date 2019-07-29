"""
The purpose of this code is to use the Spotify API to download the data 
I want to analyse
"""

import requests # Used for API calls
import json # To parse response from API call
from spfy_token import AccessToken # Module where I store my access token

# Instructions on how to obtain Auth Token can be found in docs directory
access_token = AccessToken.TOKEN

# You can search for Artist IDs using: https://developer.spotify.com/console/get-search-item/?q=AC%2FDC&type=artist&market=&limit=&offset=
# Artist ID for Queen
artist_id = "1dfeR4HaWDbWqFHLkxsg1d"

# URL Endpoint
url = "https://api.spotify.com/v1/artists/" + artist_id + "/top-tracks"

# Paramters to URL Endpoint
parameters = {"id": artist_id, "country": "AU"}

# Headers for URL Endpoint
headers = {'Accept': 'application/json',
           'Content-Type': 'application/json',
           'Authorization': 'Bearer {0}'.format(access_token)}

response = requests.get(url, params=parameters, headers=headers)

# Print the status code of the response.
print(response.status_code)

data = response.json()
tracks = data["tracks"]
print(len(tracks))

# for key, value in response.json().items():
#     print(key)
#     print(value)
#     print(type(value))
#     print(len(value))
#     for i in len(value):
#         value[i]