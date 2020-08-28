# Initial steps
# 1. create the class and main function to initiate set up ✓
# 2. actions:
#       - access daily playlist ✓
#           - items -> name
#       - check monthly playlists for correct years ✓
#           - if monthly playlist isn't made, make one ✓
#       - take all daily songs and move them to month playlist ✓
#       - remove all songs on daily playlist ✓

import json
import requests
import sys
from datetime import datetime
import calendar

from config import spotify_token


class SpotifyArchive(object):
    """Move all songs from daily playlist into a month archive"""

    def __init__(self):
        self.header = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(spotify_token)
        }
        self.playlist_dict = {}

    def createPlaylistDict(self, url):
        r = requests.get(url, headers=self.header)

        if r:
            json_dict = r.json()
        else:
            r.raise_for_status()

        # dictionary: playlist_id: {name: , id: , description: }
        for item in json_dict['items']:
            internal_dict = {}
            internal_dict['name'] = item['name']
            internal_dict['id'] = item['id']
            internal_dict['description'] = item['description']
            self.playlist_dict["playlist_{}".format(
                item['id'])] = internal_dict

        if json_dict['next'] is not None:
            self.createPlaylistDict(json_dict['next'])

        return self.playlist_dict

    def getUserDailyPlaylist(self):
        """Get id for daily playlist"""
        # Find the playlist with keyword 'daily' in the description
        for item in self.playlist_dict.values():
            desc = item['description']
            if "daily" in desc:
                # If the daily playlist exists, return the ID
                return item['id']

        return False

    def doesMonthPlaylistExist(self, user):
        """Check if the monthly playlist has been made, if not create it"""

        # Get the current month name
        current_month = datetime.now().month
        month_name = calendar.month_name[current_month]

        # I format my months based on the years differently this helps me find the month
        # from this year
        playlist_name = "✩ {} ✩".format(month_name)

        for item in self.playlist_dict.values():
            if item['name'] == playlist_name:
                return item['id']

        # create a playlist for this month, since an id has not been returned
        req_body = {
            "name": "{}".format(playlist_name),
            "public": "false"
        }

        r = requests.post(
            'https://api.spotify.com/v1/users/{}/playlists'.format(user), headers=self.header, data=json.dumps(req_body, indent=4))

        if r:
            json_dict = r.json()
        else:
            r.raise_for_status()

        return json_dict['id']

    def moveToMonthly(self, daily_id, month_id):
        # get all of the uris from the tracks in the daily playlist
        r = requests.get(
            'https://api.spotify.com/v1/playlists/{}/tracks'.format(daily_id), headers=self.header)

        if r:
            json_dict = r.json()
        else:
            r.raise_for_status()

        track_list = []
        for item in json_dict['items']:
            track_list.append(item['track']['uri'])

        req_body = {'uris': track_list}
        requests.post('https://api.spotify.com/v1/playlists/{}/tracks'.format(month_id),
                      headers=self.header, data=json.dumps(req_body, indent=4))

        return

    def removeTracks(self, daily_id):
        # create the request body from all of the current tracks
        r = requests.get(
            'https://api.spotify.com/v1/playlists/{}/tracks'.format(daily_id), headers=self.header)

        if r:
            json_dict = r.json()
        else:
            r.raise_for_status()

        tracks = []
        position = 0
        for item in json_dict['items']:
            track = {}
            uri = item['track']['uri']
            track['uri'] = uri
            track['positions'] = [position]
            tracks.append(track)
            position = position + 1

        data = {}
        data['tracks'] = tracks

        r = requests.delete('https://api.spotify.com/v1/playlists/{}/tracks'.format(daily_id),
                            headers=self.header, data=json.dumps(data, indent=4))

        r.raise_for_status()

        return


def main():
    try:
        user = sys.argv[1]
    except:
        raise Exception("The first command line argument is required")

    spotifyarchive = SpotifyArchive()
    spotifyarchive.createPlaylistDict(
        'https://api.spotify.com/v1/users/{}/playlists?limit=50&offset=0'.format(user))
    daily_id = spotifyarchive.getUserDailyPlaylist()
    month_id = spotifyarchive.doesMonthPlaylistExist(user)
    spotifyarchive.moveToMonthly(daily_id, month_id)
    spotifyarchive.removeTracks(daily_id)


if __name__ == '__main__':
    main()
