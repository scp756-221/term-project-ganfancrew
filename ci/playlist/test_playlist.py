"""
Test the *_original_artist routines.

These tests are invoked by running `pytest` with the
appropriate options and environment variables, as
defined in `conftest.py`.
"""

# Standard libraries

# Installed packages
import pytest

# Local modules
import playlist


@pytest.fixture
def pserv(request, playlist_url, auth):
    return playlist.Playlist(playlist_url, auth)


def test_playlist_full_cycle(pserv):
    song = ('Yamashita Tatsuto', 'Kanashimi no Jody')
    song2 = ('Kikuchi Mariya', 'Plastic Love')
    song3 = ('Yamashita Tatsuto', 'RIDE ON TIME')
    p_title = 'MyDefaultPlaylist'
    p_title2 = 'SecondPlaylist'

    trc = pserv.all()
    assert trc == 200

    trc, m_id = pserv.add_song(song[0], song[1], p_title)
    assert trc == 200
    trc, m_id2 = pserv.add_song(song2[0], song2[1], p_title)
    assert trc == 200
    trc, m_id3 = pserv.add_song(song3[0], song3[1], p_title2)
    assert trc == 200

    trc, songs = pserv.read_playlist(p_title)
    assert (trc == 200 and song[1] in songs
            and song2[1] in songs)

    trc, songs = pserv.read_playlist(p_title2)
    assert (trc == 200 and song3[1] in songs)

    pserv.delete_song(p_title, m_id)
    pserv.delete_song(p_title, m_id2)
    pserv.delete_song(p_title, m_id3)
