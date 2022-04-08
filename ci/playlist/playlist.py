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

    def all(self):
        """
        Show all playlists.

        Returns
        -------
        status, all_records

        status: number
            The HTTP status code returned by Playlist.
        all_records: json
            If status is 200, the all records in the database.
            If status is not 200, None.

        """
        r = requests.get(
            self._url,
            headers={'Authorization': self._auth}
            )
        if r.status_code != 200:
            return r.status_code, None

        return r.status_code, r.json()

    def add_song(self, artist, song, playlist_title):
        """
        Add a song to a playlist.

        Parameters
        ----------
        artist: string
            The artist performing song.
        song: string
            The name of the song.
        playlist_title: string
            The title of the playlist.

        Returns
        -------
        status, music_id

        status: number
            The HTTP status code returned by Playlist.
        music_id: string
            If status is 200, the UUID of the song.
            If status is not 200, None.

        """
        r = requests.post(
            self._url,
            json={'Artist': artist,
                  'SongTitle': song,
                  'PlaylistTitle': playlist_title},
            headers={'Authorization': self._auth}
        )
        if r.status_code != 200:
            return r.status_code, None

        return r.status_code, r.json()['music_id']

    def read_playlist(self, playlist_title):
        """
        List all songs in a playlist.

        Parameters
        ----------
        playlist: string
            The title of playlist in the playlist database.

        Returns
        -------
        status, song_records

        status: number
            The HTTP status code returned by Playlist.
        song_records: json
            If status is 200, the songs info in the playlist.
            If status is not 200, None.

        """
        r = requests.get(
            self._url + playlist_title,
            headers={'Authorization': self._auth}
            )
        if r.status_code != 200:
            return r.status_code, None

        return r.status_code, r.json()

    def delete_song(self, playlist_title, music_id):
        """
        Delete a song in a playlist.

        Parameters
        ----------
        playlist: string
            The title of playlist in the playlist database.
        music_id: string
            The UUID of this song in the playlist database.

        Returns
        -------
        Does not return anything. The playlist delete operation
        always returns 200, HTTP success.
        """
        requests.delete(
            self._url + playlist_title + '/' + music_id,
            headers={'Authorization': self._auth}
        )
