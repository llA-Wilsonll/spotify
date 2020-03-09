"""
The purpose of this code is to use the Spotify API to create a running playlist of popular songs playing a certain
number of beats per minute (BPM)
"""

import requests
import sys
sys.path.insert(1, './src/running_playlist')
from spfy_token_2 import AccessToken  # Module where I store my access token
#import pandas as pd  # DataFrame, concat, crosstab

# Instructions on how to obtain Auth Token can be found in docs directory
access_token = AccessToken.TOKEN

# URL Endpoint
url = "https://api.spotify.com/v1/search"

years = ["90", "00", "10"]
playlists = []

for year in years:
    # Parameters to URL Endpoint
    parameters = {"q": "All Out " + year + "s", "type": "playlist"}

    # Headers for URL Endpoint
    headers = {'Accept': 'application/json',
               'Content-Type': 'application/json',
               'Authorization': 'Bearer {0}'.format(access_token)}

    # Get the spotify data
    response = requests.get(url, params=parameters, headers=headers)
    # Print the status code of the response.
    print('STATUS CODE: ' + str(response.status_code))

    data = response.json()

    # Extracting and saving the href for a playlist if it is Owned by Spotify
    items = data["playlists"]["items"]
    for item in items:
        if item['owner']['display_name'] == "Spotify":
            playlists += [item['href']]

tracks = []
# Downloading the songs from a playlist along with its features
for playlist in playlists:
    url2 = playlist + '/tracks'
    headers2 = {'Authorization': 'Bearer {0}'.format(access_token)}
    response2 = requests.get(url2, headers=headers2)
    print('STATUS CODE: ' + str(response2.status_code))
    data2 = response2.json()
    for item in data2['items']:
        tracks.append(item['track']['id'])

print("Number of tracks =", len(tracks))
print(tracks)


"""
To do:
- Get features, particularly tempo, for all these songs
- Filter for specific tempo range
"""
