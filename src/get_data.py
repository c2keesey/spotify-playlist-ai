import json
import os
import time

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables from .env file
load_dotenv()

# Set up Spotify API client
scope = "user-library-read playlist-read-private"
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri=os.getenv("REDIRECT_URI"),
        scope=scope,
    )
)


playlists_to_fetch = [
    "New",
    "⏣ Halcyon",
    "🜂 BOOM",
    "🜍 H",
    "Indie",
    "LoFi ⏣ 🜔 ",
    "Creekwalk",
]


def get_all_playlists():
    results = sp.current_user_playlists()
    playlists = results["items"]
    while results["next"]:
        results = sp.next(results)
        playlists.extend(results["items"])
    return playlists


def get_playlist_tracks(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = results["items"]
    while results["next"]:
        results = sp.next(results)
        tracks.extend(results["items"])
    return tracks


def get_audio_features(track_ids):
    audio_features = []
    valid_track_ids = [t for t in track_ids if t is not None]
    for i in range(0, len(valid_track_ids), 100):
        batch = valid_track_ids[i : i + 100]
        features = sp.audio_features(batch)
        audio_features.extend(features)
    return audio_features


def main():
    # Get user ID
    user_id = sp.me()["id"]

    # Get all playlists
    print("Fetching playlists...")
    all_playlists = get_all_playlists()

    # Filter playlists created by the user
    user_playlists = [
        playlist for playlist in all_playlists if playlist["owner"]["id"] == user_id
    ]

    # Get tracks and audio features for each user-created playlist
    playlists_with_tracks = []
    for playlist in user_playlists:
        print(f"Fetching tracks for playlist: {playlist['name']}...")
        playlist_tracks = get_playlist_tracks(playlist["id"])
        playlist_track_ids = [
            track["track"]["id"] if track["track"] else None
            for track in playlist_tracks
        ]
        playlist_audio_features = get_audio_features(playlist_track_ids)

        playlist_tracks_with_features = []
        for track, features in zip(playlist_tracks, playlist_audio_features):
            if track["track"] and features:
                track_info = {
                    "id": track["track"]["id"],
                    "name": track["track"]["name"],
                    "artists": [artist["name"] for artist in track["track"]["artists"]],
                    "album": track["track"]["album"]["name"],
                    "audio_features": features,
                }
                playlist_tracks_with_features.append(track_info)
            else:
                print(
                    f"Skipping track due to missing data: {track['track']['name'] if track['track'] else 'Unknown'}"
                )

        playlist_info = {
            "id": playlist["id"],
            "name": playlist["name"],
            "tracks": playlist_tracks_with_features,
        }
        playlists_with_tracks.append(playlist_info)

        # Sleep to avoid rate limiting
        time.sleep(1)

    # Save data to JSON file
    library_data = {
        "playlists": playlists_with_tracks,
    }

    with open("_data/all_playlists.json", "w") as f:
        json.dump(library_data, f, indent=2)

    print("Library snapshot saved to spotify_library_snapshot.json")
    print(f"Total user-created playlists processed: {len(playlists_with_tracks)}")


if __name__ == "__main__":
    main()
