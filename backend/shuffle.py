# import spotipy
# from spotipy.oauth2 import SpotifyOAuth
# from sklearn.cluster import KMeans

# def shuffle_and_add_to_queue(playlist_id, token):
#     # Setup Spotify client with the provided token
#     spotify_client = spotipy.Spotify(auth=token)

#     # Retrieve tracks and their audio features from the playlist
#     tracks = spotify_client.playlist_tracks(playlist_id)
#     track_ids = [track['track']['id'] for track in tracks['items']]
#     audio_features = spotify_client.audio_features(track_ids)

#     # Extract relevant features for each track and apply k-means clustering
#     features_list = [[features['energy'], features['key'], features['valence'], features['tempo']] for features in audio_features]
#     kmeans = KMeans(n_clusters=5, random_state=0).fit(features_list)
#     clusters = kmeans.labels_

#     # Sort tracks by cluster
#     sorted_tracks = sorted(zip(track_ids, clusters, features_list), key=lambda x: (x[1], x[2][3]))

#     # Get list of devices
#     devices = spotify_client.devices()
#     if devices['devices']:
#         # Select the first available device
#         device_id = devices['devices'][0]['id']
#         # Transfer playback to this device
#         spotify_client.transfer_playback(device_id)

#         # Add tracks to the user's queue
#         for track_id, _, _ in sorted_tracks:
#             track_uri = f"spotify:track:{track_id}"
#             spotify_client.add_to_queue(track_uri)
#         print("Done")
#     else:
#         print("No active devices found")


# # token = "BQByO391zlHMd9aXHx20Fyp7h1g1UwrPCs9INtiQh-zddDCaUX4Tq7mkamvbHvxM3LUuZRIkL7qvRMRzpJOtK-CScl6n2bzkajNG3TEV3-SjnAz8R6BtIY45-kijouEBq7h8m6VwmjL53b1FWci4c9wKUHCsI2sn3qNYqMEJX3qAJ8-fTftwWmrRJMR7HQ1qsXYuvjYHqzW-Uloutqrrrb58sQ"
# # playlist_id = "1mSPjuL0spUjUkeK965epf"

# # shuffle_and_add_to_queue(playlist_id, token)



import spotipy
from spotipy.oauth2 import SpotifyOAuth
from sklearn.cluster import KMeans

# def shuffle_and_add_to_queue(playlist_id, token):
#     # Setup Spotify client with the provided token
#     spotify_client = spotipy.Spotify(auth=token)

#     # Retrieve tracks and their audio features from the playlist
#     tracks = spotify_client.playlist_tracks(playlist_id)
#     track_ids = [track['track']['id'] for track in tracks['items']]
#     audio_features = spotify_client.audio_features(track_ids)

#     # Extract relevant features for each track and apply k-means clustering
#     features_list = [[features['energy'], features['key'], features['valence'], features['tempo']] for features in audio_features]
#     kmeans = KMeans(n_clusters=5, random_state=0).fit(features_list)
#     clusters = kmeans.labels_

#     # Sort tracks by cluster
#     sorted_tracks = sorted(zip(track_ids, clusters, features_list), key=lambda x: (x[1], x[2][3]))
    
#     # # Get list of devices
#     # devices = spotify_client.devices()
#     # if devices['devices']:
#     #     # Select the first available device
#     #     device_id = devices['devices'][0]['id']
#     #     # Transfer playback to this device
#     #     spotify_client.transfer_playback(device_id)

#     #     # Add tracks to the user's queue
#     #     for track_id, _, _ in sorted_tracks:
#     #         track_uri = f"spotify:track:{track_id}"
#     #         spotify_client.add_to_queue(track_uri)
#     # Get list of devices
    
#     devices = spotify_client.devices()
#     active_devices = [device for device in devices['devices'] if device['is_active']]

#     if active_devices:
#         # Select the first active device
#         device_id = active_devices[0]['id']
#         # Transfer playback to this device
#         spotify_client.transfer_playback(device_id)

#         # Add tracks to the user's queue
#         for track_id, _, _ in sorted_tracks:
#             track_uri = f"spotify:track:{track_id}"
#             spotify_client.add_to_queue(track_uri)
            
#     else:
#         print("No active devices found")



def get_all_playlist_tracks(playlist_id, spotify_client):
    limit = 100  # Adjust the limit based on your needs
    offset = 0
    all_tracks = []

    while True:
        # Retrieve a batch of tracks
        tracks = spotify_client.playlist_tracks(playlist_id, offset=offset, limit=limit)

        # Break the loop if no more tracks are available
        if not tracks['items']:
            break

        # Extract track IDs from the batch
        track_ids = [track['track']['id'] for track in tracks['items']]
        audio_features = spotify_client.audio_features(track_ids)

        # Extract relevant features for each track and apply k-means clustering
        features_list = [
            [features['energy'], features['key'], features['valence'], features['tempo']] 
            for features in audio_features
        ]
        clusters = KMeans(n_clusters=5, random_state=0).fit_predict(features_list)

        # Append the tracks, their clusters, and features to the list
        all_tracks.extend(zip(track_ids, clusters, features_list))

        # Move the offset for the next batch
        offset += limit

    return all_tracks

def shuffle_and_add_to_queue(playlist_id, token):
    # Setup Spotify client with the provided token
    spotify_client = spotipy.Spotify(auth=token)

    # Retrieve all tracks and their audio features from the playlist
    all_tracks = get_all_playlist_tracks(playlist_id, spotify_client)

    # Sort tracks by cluster and tempo
    sorted_tracks = sorted(all_tracks, key=lambda x: (x[1], x[2][3]))

    # Get list of devices
    devices = spotify_client.devices()
    if devices['devices']:
        # Select the first available device
        device_id = devices['devices'][0]['id']
        # Transfer playback to this device
        spotify_client.transfer_playback(device_id)

        # Add tracks to the user's queue
        for track_id, _, _ in sorted_tracks:
            track_uri = f"spotify:track:{track_id}"
            spotify_client.add_to_queue(track_uri)
    else:
        print("No active devices found")
