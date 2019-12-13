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

    return_string = '''\nWelcome to the Spotipyzer API. Please see <a href="https://github.com/NLeRoy917/playlist-api-api">the github repo <a> for details.\n'''

    return return_string

# Testing route/main route
@app.route('/test')
def api_base_test():

    return_string = '''\nBARNABAS A BUM FR\n'''

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

	# converrt data to raw data so that the list can be used for visualization
	for track in tracks:
		continue
		# Get analysis data from Spotify
		analysis = get_track_data(track['id'],spotify_header)


	playlist_analysis_json = json.dumps(playlist_analysis)

	return "Under Construction" #playlist_analysis_json



@app.route('/<username>/<playlist_id>/features', methods=['GET'])
def feature_playlist(username,playlist_id):

	access_token = request.headers['access_token']
	spotify_header = {'Authorization': 'Bearer ' + access_token}

	tracks = get_tracks(playlist_id,spotify_header)

	playlist_analysis = {"names":[],
						"ids":[],
						"duration_ms" : [],
  						"key" : [],
  						"mode" : [],
  						"time_signature" : [],
  						"acousticness" : [],
  						"danceability" : [],
  						"energy" : [],
  						"instrumentalness" : [],
  						"liveness" : [],
  						"loudness" : [],
  						"speechiness" : [],
  						"valence" : [],
  						"tempo" : [],
  						"uri" : [],
  						"track_href" : [],
  						"analysis_url" : [],
  						"type" : []}

  	# convert data to raw data list that can be used for visualiztion
	for track in tracks:

		# Analyze the track with Spotify
		analysis = get_track_data(track['id'],spotify_header)

		# Organize data into raw data that can be visualized client-side
		playlist_analysis['names'].append(track['name'])
		playlist_analysis['ids'].append(track['id'])
		playlist_analysis['duration_ms'].append(analysis['duration_ms'])
		playlist_analysis['key'].append(int_to_key(analysis['key']))
		playlist_analysis['mode'].append(int_to_mode(analysis['mode']))
		playlist_analysis['time_signature'].append(analysis['time_signature'])
		playlist_analysis['acousticness'].append(analysis['acousticness'])
		playlist_analysis['danceability'].append(analysis['danceability'])
		playlist_analysis['energy'].append(analysis['energy'])
		playlist_analysis['instrumentalness'].append(analysis['instrumentalness'])
		playlist_analysis['liveness'].append(analysis['liveness'])
		playlist_analysis['loudness'].append(analysis['loudness'])
		playlist_analysis['speechiness'].append(analysis['speechiness'])
		playlist_analysis['valence'].append(analysis['valence'])
		playlist_analysis['tempo'].append(analysis['tempo'])
		playlist_analysis['uri'].append(analysis['uri'])
		playlist_analysis['track_href'].append(analysis['track_href'])
		playlist_analysis['analysis_url'].append(analysis['analysis_url'])
		playlist_analysis['type'].append(analysis['type'])

	# Pack into JSON format
	playlist_analysis_json = json.dumps(playlist_analysis)

	return playlist_analysis_json


if __name__ == '__main__':
    app.run()
