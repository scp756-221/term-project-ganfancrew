"""
Simple command-line interface to playlist service
"""

# Standard library modules
import argparse
import cmd
import re

# Installed packages
import requests

# The services check only that we pass an authorization,
# not whether it's valid
DEFAULT_AUTH = 'Bearer A'


def parse_args():
    argp = argparse.ArgumentParser(
        'pcli',
        description='Command-line query interface to playlist service'
        )
    argp.add_argument(
        'name',
        help="DNS name or IP address of playlist server"
        )
    argp.add_argument(
        'port',
        type=int,
        help="Port number of playlist server"
        )
    return argp.parse_args()


def get_url(name, port):
    return "http://{}:{}/api/v1/playlist/".format(name, port)


def parse_quoted_strings(arg):
    """
    Parse a line that includes words and '-, and "-quoted strings.
    This is a simple parser that can be easily thrown off by odd
    arguments, such as entries with mismatched quotes.  It's good
    enough for simple use, parsing "-quoted names with apostrophes.
    """
    mre = re.compile(r'''(\w+)|'([^']*)'|"([^"]*)"''')
    args = mre.findall(arg)
    return [''.join(a) for a in args]


class Pcli(cmd.Cmd):
    def __init__(self, args):
        self.name = args.name
        self.port = args.port
        cmd.Cmd.__init__(self)
        self.prompt = 'mql: '
        self.intro = """
Command-line interface to playlist service.
Enter 'help' for command list.
'Tab' character autocompletes commands.
"""

    def do_playlists(self, arg):
        """
        Show all playlists.

        Examples
        --------
        playlists
            Show all titles of existing playlists.
        """
        url = get_url(self.name, self.port)
        r = requests.get(
            url,
            headers={'Authorization': DEFAULT_AUTH}
            )
        if r.status_code != 200:
            print("Non-successful status code:", r.status_code)
        items = r.json()
        if 'Count' not in items:
            print("No playlists")
            return
        if items['Count'] == 0:
            print("No playlists")
        else:
            playlist = set(i['PlaylistTitle'] for i in items['Items'])
            print(playlist)

    def do_read_playlist(self, arg):
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
        url = get_url(self.name, self.port)
        playlist = arg.strip()
        if playlist == '':
            print("Wrong number of parameters")
            return
        r = requests.get(
            url+playlist,
            headers={'Authorization': DEFAULT_AUTH}
            )
        if r.status_code != 200:
            print("Non-successful status code:", r.status_code)
        items = r.json()
        if 'Count' not in items:
            print("{} does not exist".format(playlist))
            return
        num_song = items['Count']
        if num_song == 0:
            print("{} does not exist".format(playlist))
        else:
            print("{} song(s) in {}".format(num_song, playlist))
            for i in items['Items']:
                print("{} {} {:20.20s} {}".format(
                    i['PlaylistTitle'],
                    i['music_id'],
                    i['Artist'],
                    i['SongTitle']))

    def do_add_song(self, arg):
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
        url = get_url(self.name, self.port)
        args = parse_quoted_strings(arg)
        if len(args) < 2:
            print("Wrong number of parameters")
            return
        payload = {
            'Artist': args[0],
            'SongTitle': args[1]
        }
        if len(args) == 3:
            payload['PlaylistTitle'] = args[2]
        else:
            payload['PlaylistTitle'] = "MyDefaultPlaylist"
        r = requests.post(
            url,
            json=payload,
            headers={'Authorization': DEFAULT_AUTH}
        )
        if r.status_code != 200:
            print("Non-successful status code: {}, {}"
                  .format(r.status_code, r.json()["error"]))
        else:
            print(r.json())

    def do_delete_song(self, arg):
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
        url = get_url(self.name, self.port)
        args = arg.strip().split()
        if len(args) != 2:
            print("Wrong number of parameters")
            return
        r = requests.delete(
            url+args[0]+'/'+args[1],
            headers={'Authorization': DEFAULT_AUTH}
        )
        if r.status_code != 200:
            print("Non-successful status code:", r.status_code)
        else:
            print('Delete song successfully')

    def do_delete_playlist(self, arg):
        """
        Delete a playlist.

        Parameters
        ----------
        playlist: string
            The title of the playlist

        Examples
        --------
        delete_playlist MyPlaylist
            Delete the MyPlaylist playlist.
        """
        url = get_url(self.name, self.port)
        playlist = arg.strip()
        if playlist == '':
            print("Wrong number of parameters")
            return
        r = requests.get(
            url+playlist,
            headers={'Authorization': DEFAULT_AUTH}
        )
        if r.status_code != 200:
            print("Non-successful status code:", r.status_code)
        items = r.json()
        if 'Count' not in items:
            print("{} does not exist".format(playlist))
            return
        num_song = items['Count']
        if num_song == 0:
            print("{} does not exist".format(playlist))
        else:
            print("{} song(s) in {}".format(num_song, playlist))
            for i in items['Items']:
                del_r = requests.delete(
                    url+playlist+'/'+i['music_id'],
                    headers={'Authorization': DEFAULT_AUTH}
                )
                if del_r.status_code != 200:
                    print("Non-successful status code:", del_r.status_code)
                    return
                else:
                    print('Delete song successfully')

    def do_quit(self, arg):
        """
        Quit the program.
        """
        return True

    # def do_test(self, arg):
    #     """
    #     Run a test stub on the playlist server.
    #     """
    #     url = get_url(self.name, self.port)
    #     r = requests.get(
    #         url+'test',
    #         headers={'Authorization': DEFAULT_AUTH}
    #         )
    #     if r.status_code != 200:
    #         print("Non-successful status code:", r.status_code)

    def do_shutdown(self, arg):
        """
        Tell the playlist cerver to shut down.
        """
        url = get_url(self.name, self.port)
        r = requests.get(
            url+'shutdown',
            headers={'Authorization': DEFAULT_AUTH}
            )
        if r.status_code != 200:
            print("Non-successful status code:", r.status_code)


if __name__ == '__main__':
    args = parse_args()
    Pcli(args).cmdloop()
