# spotify-playlist-ai

## Description

This project classifies liked songs into a user's existing Spotify playlists. It compares multiple machine learning methods including Random Forest, Gradient Boosting, Support Vector Machines, and Neural Networks.

- In the '\_data' folder, the 'main_set.json' file contains the data for testing the models.
  It has the form:

```
{
  "playlists": [
    {
      "id": "1ykexMp16g3EB7SqQOFsdN",
      "name": "Vantage \u23e3 \ud83d\udf14 \u232c",
      "tracks": [
        {
          "id": "2IpfiNS4x20FJ5qKTHWaJ3",
          "name": "Diamonds",
          "artists": ["Lane 8", "Solomon Grey"],
          "album": "Rise",
          "audio_features": {
            "danceability": 0.663,
            "energy": 0.675,
            "key": 2,
            "loudness": -7.744,
            "mode": 0,
            "speechiness": 0.0425,
            "acousticness": 0.022,
            "instrumentalness": 0.489,
            "liveness": 0.0611,
            "valence": 0.513,
            "tempo": 120.009,
            "type": "audio_features",
            "id": "2IpfiNS4x20FJ5qKTHWaJ3",
            "uri": "spotify:track:2IpfiNS4x20FJ5qKTHWaJ3",
            "track_href": "https://api.spotify.com/v1/tracks/2IpfiNS4x20FJ5qKTHWaJ3",
            "analysis_url": "https://api.spotify.com/v1/audio-analysis/2IpfiNS4x20FJ5qKTHWaJ3",
            "duration_ms": 354060,
            "time_signature": 4
          }
        },
```

- The dataset has already been created with get_data.py and dataset.py
