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

        Examples
        --------
        playlists
            Show all titles of existing playlists.
        """
        r = requests.get(
            self._url,
            headers={'Authorization': self._auth}
            )
        return r.status_code

    def add_song(self, artist, song, playlist_title):
        """
        Add a song to a playlist.

        Parameters
        ----------
        artist: string
        song: string
            The title of the song
        playlist: string (optional)
            The title of the playlist
            The default playlist is "MyDefaultPlaylist".

        The parameters can be quoted by either single or double quotes.
        The playlist parameter should not contain any space.

        Examples
        --------
        add_song 'Stray Kids' "Charmer" "NewPlaylist"
            Add a song to the NewPlaylist playlist.
            Quote the apostrophe with double-quotes.

        add_song 'Stray Kids' 'Christmas EveL'
            Add a song to the default playlist.

        add_song aespa Savage
            No quotes needed for single-word artist or title name.
        """
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
        """
        List all songs in a playlist.

        Parameters
        ----------
        playlist: string
            The title of the playlist

        Examples
        --------
        read_playlist MyPlaylist
            List all songs in the MyPlaylist playlist.
        """
        r = requests.get(
            self._url + playlist_title,
            headers={'Authorization': self._auth}
            )
        songs = []
        res = r.json()
        for item in res['Items']:
            songs.append(item['SongTitle'])
        return r.status_code, songs

    def delete_song(self, playlist_title, music_id):
        """
        Delete a song in a playlist.

        Parameters
        ----------
        playlist: string
            The title of the playlist.
        music_id: string
            The uuid of the song to delete.

        Examples
        --------
        delete_song MyPlaylist 92dc6269-2d0f-4ac9-bf0b-ef5d9dbbc0d8
            Delete the song in the MyPlaylist playlist.
        """
        requests.delete(
            self._url + playlist_title + '/' + music_id,
            headers={'Authorization': self._auth}
        )
