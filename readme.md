## Setup

setup environment:

1. create the directory for the virtual env `python3 -m venv env`
2. use the virtual environment `source env/bin/activate`

download the required packages:

1. `pip install -r requirements.txt`

request spotify developer token:

1. go to https://developer.spotify.com/console and select and API
2. at the bottom request a token and select all of the scopes that begin with 'playlist'
3. copy and paste that token into the `config.py` file

Lastly, run `test_spotify_archive.py`. If all tests pass then the set up was successful.
