import json


def print_playlist_track_counts(fpath):
    # Load the JSON data from the file
    with open(fpath, "r") as file:
        data = json.load(file)

    # Get the playlists
    playlists = data.get("playlists", [])

    # Print the header
    print("Playlist Track Counts")
    print("--------------------")

    # Iterate through playlists and print their track counts
    for playlist in playlists:
        name = playlist.get("name", "Unnamed Playlist")
        track_count = len(playlist.get("tracks", []))
        print(f"{name}: {track_count} tracks")

    # Print total number of playlists
    print("--------------------")
    print(f"Total playlists: {len(playlists)}")
