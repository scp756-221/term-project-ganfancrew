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
    song = ('Elvis Presley', 'Hound Dog')
    p_title = 'Afternoon'

    trc, m_id = pserv.add_song(song[0], song[1], p_title)
    assert trc == 200

    trc, s_title = pserv.read_playlist(p_title)
    assert trc == 200 and s_title == song[0]

    pserv.delete_song(p_title, m_id)
