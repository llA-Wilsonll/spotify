"""
The purpose of this code manipulate the pandas DataFrames created in
make_dataset.py so that they can be used for analysis and modelling.
More specifically:
    - Clean the data where necessary
    - Join the DataFrames to create a single DataFrame that can be analysed
"""

import pandas as pd


"""
Reading the pickle files
"""
# Top tracks
top_tracks_df = pd.read_pickle("../../data/raw/top_tracks.pkl")

# Tracks from the playlist
playlist_tracks_df = pd.read_pickle("../../data/raw/playlist_tracks.pkl")

# Track Features
track_features_df = pd.read_pickle("../../data/raw/track_features.pkl")


"""
Processing the DataFrames
"""

# Making "id" is the first column
top_tracks_df = top_tracks_df[['id', 'name', 'country', 'number', 'duration_ms', 'popularity']]
playlist_tracks_df = playlist_tracks_df[['id', 'name', 'duration_ms', 'popularity']]

# Confirming that the API returned the same top songs in same order for each country
print(pd.crosstab(top_tracks_df.name, top_tracks_df.number))

# As top songs are same for each country, subset top_tracks_df for country = AU
top_tracks_df = top_tracks_df.loc[top_tracks_df['country'] == "AU"]

# Creating name_sub as part of name before the '-'
# Due to different versions of the same songs in top_tracks_df and track_features_df
# and so can't do direct join on either id or name
top_tracks_df['name_sub'] = top_tracks_df['name'].str.split(" - ", expand=True)[0]
playlist_tracks_df['name_sub'] = playlist_tracks_df['name'].str.split(" - ", expand=True)[0]

# Reducing DataFrames so only required columns are present
top_tracks_df = top_tracks_df.loc[:, ['name_sub', 'number']]
playlist_tracks_df = playlist_tracks_df.loc[:, ['id', 'name_sub']]
track_features_df = track_features_df.loc[:, ['id', 'danceability', 'energy', 'key', 'loudness', 'mode',
                                              'speechiness', 'acousticness', 'instrumentalness', 'liveness',
                                              'valence', 'tempo', 'duration_ms', 'time_signature']]

# Removing duplicate "id" column
track_features_df = track_features_df.loc[:, ~track_features_df.columns.duplicated()]


"""
Joining the DataFrames
"""

# Joining track ID onto top_tracks_df from playlist_tracks_df, using name_sub as the join key
playlist_tracks_df = pd.merge(playlist_tracks_df, top_tracks_df, how='left', on='name_sub')

# Joining number onto track_features_df from top_tracks_df, using id as the join key
track_features_df = pd.merge(track_features_df, playlist_tracks_df, how='left', on='id')

# Creating indicator variable to signify if track is in Spotify's top 10 tracks for The Beatles
track_features_df['top_track_ind'] = (~track_features_df['number'].isna()).astype(int)


"""
Pickle the track_features_df DataFrame
    - Saving to the /data/processed subdirectory
"""

# Track Features
track_features_df.to_pickle("../../data/processed/track_features_processed.pkl")
