"""
Test the playlist routines.

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


@pytest.fixture
def song(request):
    return ('IVE', 'LOVE DIVE')


@pytest.fixture
def song_list(request):
    return [('Kep1er', 'WA DA DA'), ('STAYC', 'RUN2U'), ('IVE', 'ELEVEN')]


def test_simple_run(pserv, song):
    trc, lp = pserv.all()
    assert trc == 200 and lp['Count'] == 0

    playlist_title = 'NewPlaylist1'
    trc, m_id = pserv.add_song(song[0], song[1], playlist_title)
    assert trc == 200

    trc, rp = pserv.read_playlist(playlist_title)
    assert trc == 200
    m_list = []
    for p in rp['Items']:
        assert p['PlaylistTitle'] == playlist_title
        m_list.append(p['music_id'])
    assert m_id in m_list

    pserv.delete_song(playlist_title, m_id)


def test_full_run(pserv, song, song_list):
    trc, lp = pserv.all()
    assert trc == 200 and lp['Count'] == 0

    ptitle1 = 'NewPlaylist1'
    ptitle2 = 'NewPlaylist2'
    trc, rp = pserv.read_playlist(ptitle1)
    assert trc == 200 and rp['Count'] == 0
    trc, rp = pserv.read_playlist(ptitle2)
    assert trc == 200 and rp['Count'] == 0

    m_list = []
    for s in song_list:
        trc, m_id = pserv.add_song(s[0], s[1], ptitle1)
        assert trc == 200
        m_list.append(m_id)

    trc, m_id = pserv.add_song(song[0], song[1], ptitle2)
    assert trc == 200

    trc, rp = pserv.read_playlist(ptitle2)
    assert trc == 200 and rp['Count'] == 1

    trc, rp = pserv.read_playlist(ptitle1)
    assert trc == 200 and rp['Count'] == 3
    for p in rp['Items']:
        assert (p['PlaylistTitle'] == ptitle1 and
                p['music_id'] in m_list)

    trc, lp = pserv.all()
    assert trc == 200 and lp['Count'] == 4

    for m in m_list:
        pserv.delete_song(ptitle1, m)

    trc, rp = pserv.read_playlist(ptitle1)
    assert trc == 200 and rp['Count'] == 0

    trc, lp = pserv.all()
    assert trc == 200 and lp['Count'] == 1

    trc, rp = pserv.read_playlist(ptitle2)
    assert trc == 200 and rp['Count'] == 1

    pserv.delete_song(ptitle2, m_id)

    trc, lp = pserv.all()
    assert trc == 200 and lp['Count'] == 0
