# Import costume libraries
from lib.playlists import *
from lib.track_analysis import *

# import flask
from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

#import other necessary modules
import json

# Testing route/main route
@app.route('/')
def api_base():

	#return_string = '''\nWelcome to the spottydata API. Please see <a href="https://github.com/NLeRoy917/playlist-analyzer-api">the github repo <a> for details.\n'''

	return render_template("base.html")

# Testing route/main route
@app.route('/test')
def api_base_test():

	return_string = '''\nBARNABAS A BUM FR\n'''

	return return_string

@app.route('/callback')
def api_call_back():

	auth_code = request.args.get('code')

	return auth_code

# Get playlists for a specific use
@app.route('/<username>/playlists', methods=['GET'])
def playlists_get(username):
	
	access_token = request.headers['access_token']
	spotify_header = {'Authorization': 'Bearer ' + access_token}
	playlists = get_playlists(username,spotify_header)
	playlist_json = json.dumps(playlists)

	return playlist_json



@app.route('/<playlist_id>/analysis', methods=['GET'])
def analyze_playlist(playlist_id):

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

@app.route('/<playlist_id>/analysis/keys', methods=['GET'])
def get_key_data(playlist_id):

	# Get access token from the headers and generate spotify's required header
	access_token = request.headers['access_token']
	spotify_header = {'Authorization': 'Bearer ' + access_token}

	# Extract the tracks from the playlist
	tracks = get_tracks(playlist_id,spotify_header)

	# Init key object
	key_data = {'minor': {'A':0,
						'A#':0,
						'B':0,
						'C':0,
						'C#':0,
						'D':0,
						'D#':0,
						'E':0,
						'F':0,
						'F#':0,
						'G':0,
						'G#':0},

				'major': {'A':0,
						'A#':0,
						'B':0,
						'C':0,
						'C#':0,
						'D':0,
						'D#':0,
						'E':0,
						'F':0,
						'F#':0,
						'G':0,
						'G#':0}
				}

				
	# Iterate and parse data
	for track in tracks:
		analysis = get_track_data(track['id'],spotify_header)

	# Some songs may not have a ket or mode, so catch key_not_exist error and pass 
	# (this would occur for a track that is a podcast or local file)
	try:
		if analysis['mode'] == 0:
			key_data['minor'][int_to_key(analysis['key'])] += 1
		elif analysis['mode'] == 1:
			key_data['major'][int_to_key(analysis['key'])] += 1
		else:
			continue
	except:
		pass


	# Return JSON Package
	return jsonify(key_data)


@app.route('/<playlist_id>/features', methods=['GET'])
def feature_playlist(playlist_id):

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
		#print("TRACK " + '-='*30)
		#print(track)
		# initialize keys to check for
		#analysis_keys = ['name','id','duration_ms','key','mode','time_signature','acousticness','danceability','energy','instrumentalness','liveness','loudness','speechiness','valence','tempo','uri','track_href','analysis_url','type']

		# Check that all data is there before appending to playlist_analysis
		#if all(key in track for key in analysis_keys):
			# Organize data into raw data that can be visualized client-side
		try:
			playlist_analysis['names'].append(track['name'])
		except:
			pass

		try:
			playlist_analysis['ids'].append(track['id'])
		except:
			pass

		try:
			playlist_analysis['duration_ms'].append(analysis['duration_ms'])
		except:
			pass

		try:
			playlist_analysis['key'].append(int_to_key(analysis['key']))
		except:
			pass

		try:
			playlist_analysis['mode'].append(int_to_mode(analysis['mode']))
		except:
			pass

		try:
			playlist_analysis['time_signature'].append(analysis['time_signature'])
		except:
			pass

		try:
			playlist_analysis['acousticness'].append(analysis['acousticness'])
		except:
			pass

		try:
			playlist_analysis['danceability'].append(analysis['danceability'])
		except:
			pass

		try:
			playlist_analysis['energy'].append(analysis['energy'])
		except:
			pass

		try:
			playlist_analysis['instrumentalness'].append(analysis['instrumentalness'])
		except:
			pass

		try:
			playlist_analysis['liveness'].append(analysis['liveness'])
		except:
			pass

		try:
			playlist_analysis['loudness'].append(analysis['loudness'])
		except:
			pass

		try:
			playlist_analysis['speechiness'].append(analysis['speechiness'])
		except:
			pass

		try:
			playlist_analysis['valence'].append(analysis['valence'])
		except:
			pass

		try:
			playlist_analysis['tempo'].append(analysis['tempo'])
		except:
			pass

		try:
			playlist_analysis['uri'].append(analysis['uri'])
		except:
			pass

		try:
			playlist_analysis['track_href'].append(analysis['track_href'])
		except:
			pass

		try:
			playlist_analysis['analysis_url'].append(analysis['analysis_url'])
		except:
			pass

		try:
			playlist_analysis['type'].append(analysis['type'])
		except:
			pass



	# Pack into JSON format
	playlist_analysis_json = jsonify(playlist_analysis)

	return playlist_analysis_json


if __name__ == '__main__':
    app.run()
