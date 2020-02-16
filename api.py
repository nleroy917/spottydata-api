# Import custom libraries
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

# Get playlists for a specific user
@app.route('/<username>/playlists', methods=['GET'])
def playlists_get(username):
	
	access_token = request.headers['access_token']
	spotify_header = {'Authorization': 'Bearer ' + access_token}
	playlists = get_playlists(username,spotify_header)
	playlist_json = json.dumps(playlists)

	return playlist_json


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

@app.route('/<playlist_id>/analysis/feel', methods=['GET'])
def get_feel_data(playlist_id):

	# Get access token from the headers and generate spotify's required header
	access_token = request.headers['access_token']
	spotify_header = {'Authorization': 'Bearer ' + access_token}

	# Extract the tracks from the playlist
	tracks = get_tracks(playlist_id,spotify_header)

	feel_data = {
				  "acousticness" : 0,
				  "danceability" : 0,
				  "energy" : 0,
				  "instrumentalness" : 0,
				  "liveness" : 0,
				  "loudness" : 0,
				  "speechiness" : 0
				}

	cnt = 0

	for track in tracks:

		# Analyze the track with Spotify
		analysis = get_track_data(track['id'],spotify_header)

		try:
			feel_data['acousticness'] += analysis['acousticness']
			feel_data['danceability'] += analysis['danceability']
			feel_data['energy'] += analysis['energy']
			feel_data['instrumentalness'] += analysis['instrumentalness']
			feel_data['liveness'] += analysis['liveness']
			feel_data['loudness'] += abs(analysis['loudness'])
			feel_data['speechiness'] += analysis['speechiness']

		except:
			pass

		cnt += 1


	# Divide the sum by the number of tracks
	for key in feel_data:
		feel_data[key] /= cnt



	return jsonify(feel_data)

@app.route('/<playlist_id>/analysis/genre', methods=['GET'])
def get_genre_data(playlist_id):

	# Get access token from the headers and generate spotify's required header
	access_token = request.headers['access_token']
	spotify_header = {'Authorization': 'Bearer ' + access_token}

	# Extract the tracks from the playlist
	tracks = get_tracks(playlist_id,spotify_header)

	genre_data = {}

	for track in tracks:

		try:
			# Get track artist
			artist_id = track['artists'][0]['id']

			# Get Artist data + genres
			artist = get_artist(artist_id,spotify_header)

			genres = artist['genres']

			# Append artist genres to the genre dictionary
			for genre in genres:

				# check that the genre exists in the dictionary
				if genre not in genre_data:
					genre_data[genre] = 1
				else:
					genre_data[genre] += 1
		except:
			continue

	#print(genre_data)

	return jsonify(genre_data)

@app.route('/<playlist_id>/analysis/tempo', methods=['GET'])
def get_tempo_data(playlist_id):

	# Get access token from the headers and generate spotify's required header
	access_token = request.headers['access_token']
	spotify_header = {'Authorization': 'Bearer ' + access_token}

	# Extract the tracks from the playlist
	tracks = get_tracks(playlist_id,spotify_header)

	tempo_store = []
	tempo_data = {}

	for track in tracks:

		try:
			#analyze track and store tempo
			analysis = get_track_data(track['id'],spotify_header)
			tempo_store.append(analysis['tempo'])
		except:
			continue


	# create hist object from array of data
	density = generate_density(tempo_store)
	
	# populate payload | dont forget to convert numpy arrays to lists
	tempo_data={'x': density.x,
				'y': density.y}
	
	return jsonify(tempo_data)


if __name__ == '__main__':
	app.run()
