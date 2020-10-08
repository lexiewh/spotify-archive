## Setup

**setup environment**:

1. create the directory for the virtual env `python3 -m venv env`
2. use the virtual environment `source env/bin/activate`

**download the required packages**:

1. `pip install -r requirements.txt`

**request spotify developer token**:

1. go to https://developer.spotify.com/console and select and API
2. at the bottom request a token and select all of the scopes that begin with 'playlist'
3. this token will be used as the second command line argument

**Lastly, run `test_spotify_archive.py`. If all tests pass then the set up was successful.**

## Debug

If you want to use the debug features in vscode, follow the following instructions.

1. create a `launch.json` file (in the .vscode directory)
2. use the python script template
3. add `"args":` with a list of arguments as such: `["username", "token"]`
4. run this script in the debug console
