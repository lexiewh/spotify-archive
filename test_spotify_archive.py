import unittest
import spotify_archive


class TestPlaylist(unittest.TestCase):

    def test_playlist_res(self):
        sa = spotify_archive.SpotifyArchive()
        res = sa.getUserDailyPlaylist()
        self.assertIsNotNone(res)

    def test_playlist_dict(self):
        sa = spotify_archive.SpotifyArchive()
        res = sa.createPlaylistDict(
            'https://api.spotify.com/v1/users/lexwhite028/playlists?limit=50&offset=0')
        self.assertGreater(len(res), 100)


if __name__ == "__main__":
    unittest.main()
