"""
Python  API for the playlist service.
"""

# Standard library modules

# Installed packages
import requests


class Playlist():
    """Python API for the playlist service.

    Handles the details of formatting HTTP requests and decoding
    the results.

    Parameters
    ----------
    url: string
        The URL for accessing the playlist service. Often
        'http://cmpt756s3:30003/'. Note the trailing slash.
    auth: string
        Authorization code to pass to the playlist service. For many
        implementations, the code is required but its content is
        ignored.
    """
    def __init__(self, url, auth):
        self._url = url
        self._auth = auth

    # def read_playlist(self, playlist_title):
    #     r = requests.get(
    #         self._url + playlist_title,
    #         headers={'Authorization': self._auth}
    #         )
    #     items = r.json()
    #     songs = []
    #     if 'Count' in items:
    #         for item in r.json()['Items']:
    #             songs.append(item['SongTitle'])
    #     if r.status_code != 200:
    #         return r.status_code, None
    #     return r.status_code, songs

    def all(self):
        r = requests.get(
            self._url,
            headers={'Authorization': self._auth}
            )
        return r.status_code

    def add_song(self, artist, song, playlist_title):
        payload = {'objtype': 'playlist',
                   'Artist': artist,
                   'SongTitle': song,
                   'PlaylistTitle': playlist_title}
        r = requests.post(
            self._url,
            json=payload,
            headers={'Authorization': self._auth}
            )
        return r.status_code, r.json()['music_id']

    def read_playlist(self, playlist_title):
        r = requests.get(
            self._url + playlist_title,
            headers={'Authorization': self._auth}
            )
        return r.status_code

    def delete_song(self, playlist_title, music_id):
        requests.delete(
            self._url + playlist_title + '/' + music_id,
            headers={'Authorization': self._auth}
        )
