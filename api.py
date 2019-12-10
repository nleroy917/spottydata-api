# Import costume libraries
from lib.playlists import *
from lib.track_analysis import *

# import flask
from flask import Flask
from flask import request
app = Flask(__name__)

#import other necessary modules
import json

# Testing route/main route
@app.route('/')
def api_base():

    return_string = '''\nTHOR IS THE STRONGEST AVENGER\n'''

    return return_string

# Get playlists for a specific use
@app.route('/<username>/playlists', methods=['GET'])
def playlists_get(username):
	
	access_token = request.headers['access_token']
	spotify_header = {'Authorization': 'Bearer ' + access_token}
	playlists = get_playlists(username,spotify_header)
	playlist_json = json.dumps(playlists)

	return playlist_json

@app.route('/<username>/<playlist_id>/analysis', methods=['GET'])
def analyze_playlist(username,playlist_id):

	access_token = request.headers['access_token']
	spotify_header = {'Authorization': 'Bearer ' + access_token}

	tracks = get_tracks(playlist_id,spotify_header)

	playlist_analysis = []

	for track in tracks:
		analysis = get_track_data(track['id'],spotify_header)
		store_dict = {'track': track,
					  'analysis':analysis}
		playlist_analysis.append(store_dict)

	playlist_analysis_json = json.dumps(playlist_analysis)

	return playlist_analysis_json




if __name__ == '__main__':
    app.run()