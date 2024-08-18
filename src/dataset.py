import json
import numpy as np
import torch
from sklearn.preprocessing import StandardScaler
from torch.utils.data import Dataset


class SpotifyPlaylistDataset(Dataset):
    def __init__(self, json_file, transform=None):
        with open(json_file, "r") as f:
            self.data = json.load(f)

        self.playlists = self.data["playlists"]
        self.tracks = []
        self.playlist_ids = []
        self.playlist_names = []
        self.genres = []

        for idx, playlist in enumerate(self.playlists):
            for track in playlist["tracks"]:
                self.tracks.append(track)
                self.playlist_ids.append(idx)
                self.playlist_names.append(playlist["name"])
                self.genres.append(track["genres"])

        # Extract relevant numerical features
        feature_keys = [
            "danceability",
            "energy",
            "loudness",
            "mode",
            "speechiness",
            "acousticness",
            "instrumentalness",
            "liveness",
            "valence",
            "tempo",
        ]
        self.features = np.array(
            [
                [track["audio_features"][key] for key in feature_keys]
                for track in self.tracks
            ]
        )

        self.scaler = StandardScaler()
        self.features = self.scaler.fit_transform(self.features)

        # Create a set of all unique genres
        all_genres = set()
        for genre_list in self.genres:
            all_genres.update(genre_list)
        self.genre_list = sorted(list(all_genres))

        # Create one-hot encoded genre features
        self.genre_features = np.zeros((len(self.tracks), len(self.genre_list)))
        for i, genre_list in enumerate(self.genres):
            for genre in genre_list:
                self.genre_features[i, self.genre_list.index(genre)] = 1

        # Combine audio features and genre features
        self.combined_features = np.hstack((self.features, self.genre_features))

        self.transform = transform

    def __len__(self):
        return len(self.tracks)

    def __getitem__(self, idx):
        track = self.tracks[idx]
        features = torch.tensor(self.combined_features[idx], dtype=torch.float32)
        playlist_id = self.playlist_ids[idx]

        if self.transform:
            features = self.transform(features)

        return features, playlist_id

    def get_playlist_names(self):
        return list(set(self.playlist_names))

    def get_playlist_features(self):
        playlist_features = {}
        for name in set(self.playlist_names):
            indices = [i for i, x in enumerate(self.playlist_names) if x == name]
            playlist_features[name] = np.mean(self.combined_features[indices], axis=0)
        return playlist_features

    def get_genre_list(self):
        return self.genre_list
