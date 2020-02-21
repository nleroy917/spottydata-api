from dotenv import load_dotenv
import os
load_dotenv()
GENIUS_API_SECRET=os.getenv('GENIUS_API_SECRET')

# Import custom libraries
from lib.playlists import *
from lib.track_analysis import *
from lib.lyrics import *

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

# testing route to load test the API for getting tracks
@app.route('/playlists/<playlist_id>/tracks', methods=['GET'])
def get_tracks(username):
	
	access_token = request.headers['access_token']
	spotify_header = {'Authorization': 'Bearer ' + access_token}

	tracks = get_tracks(playlist_id,spotify_header)

	return jsonify(tracks)

@app.route('/<playlist_id>/analysis/lyrics', methods=['GET'])
def lyrics_analysis(playlist_id):

	# Get access token from the headers and generate spotify's required header
	access_token = request.headers['access_token']
	spotify_header = {'Authorization': 'Bearer ' + access_token}

	# Extract the tracks from the playlist
	tracks = get_tracks(playlist_id,spotify_header)

	cnt = 1

	lyrics_count = {}

	for track in tracks[0:10]:
		#print('Track {}/{}'.format(cnt,len(tracks)))
		lyrics = get_lyrics(track,GENIUS_API_SECRET)
		words = parse_lyrics(lyrics)

		for word in words:
			if word in lyrics_count:
				lyrics_count[word.capitalize()] += 1
			else:
				lyrics_count[word.capitalize()] = 1

	cnt += 1
	lyrics_count_sorted = {k: v for k, v in sorted(lyrics_count.items(), key=lambda item: item[1])}

	# format payload for React library usage
	lyrics_analysis = []
	for key in lyrics_count_sorted:
		lyrics_analysis.append({'text':key,'value':lyrics_count_sorted[key]})

	return jsonify(lyrics_analysis[0:30])


@app.route('/<playlist_id>/analysis', methods=['GET'])
def full_analysis(playlist_id):

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

	feel_data = {
			  "acousticness" : 0,
			  "danceability" : 0,
			  "energy" : 0,
			  "instrumentalness" : 0,
			  "liveness" : 0,
			  "speechiness" : 0
			}
	cnt = 0

	genre_data = {}

	tempo_store = []
	tempo_data = {}
	i = 1
	# Iterate and parse data
	for track in tracks:
		print('analysis {}/{}'.format(i,len(tracks)))
		# Get the analysis for the track ONCE
		analysis = get_track_data(track['id'],spotify_header)
		i += 1

		## STORE KEY DATA ##
		# Some songs may not have a key or mode, so catch key_not_exist error and pass 
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

		## STORE FEEL DATA ##
		try:
			feel_data['acousticness'] += analysis['acousticness']
			feel_data['danceability'] += analysis['danceability']
			feel_data['energy'] += analysis['energy']
			feel_data['instrumentalness'] += analysis['instrumentalness']
			feel_data['liveness'] += analysis['liveness']
			feel_data['speechiness'] += analysis['speechiness']

		except:
			pass

		## STORE GENRE DATA ##
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

		cnt += 1

		## STORE TEMPO DATA ##
		try:
			#analyze track and store tempo
			tempo_store.append(analysis['tempo'])
		except:
			continue

	## POST PROCESSING ##

	# Divide the sum by the number of tracks
	for key in feel_data:
		feel_data[key] /= cnt

	# create hist object from array of data
	density = generate_density(tempo_store)
	
	# populate payload | dont forget to convert numpy arrays to lists
	tempo_data={'x': density.x,
				'y': density.y}


	payload = {}
	payload['keys'] = key_data
	payload['feel'] = feel_data
	payload['genres'] = genre_data
	payload['tempo'] = tempo_data

	return jsonify(payload)



if __name__ == '__main__':
	app.run()
