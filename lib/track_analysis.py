from lib.authorize import *
from lib.playlists import *
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from configparser import SafeConfigParser
import numpy as np

sns.set(color_codes=True)
sns.set_palette("dark")

def get_track_data(track_id,auth_header):

	response = requests.get('https://api.spotify.com/v1/audio-features/{}'.format(track_id),
                            headers=auth_header)

	return_package = json.loads(response.text)

	#print(return_package)

	analysis = return_package

	return analysis

def loudness_analysis(tracks,auth_header,show_plot=False):

	loudness_store = []

	for track in tracks:
		analysis = get_track_data(track['id'],auth_header)
		loudness_store.append(analysis['loudness'])

	loudness_data = {'average':None,
					 'median':None,
					 'std':None}

	loudness_data['average'] = np.average(loudness_store)
	loudness_data['median'] = np.median(loudness_store)
	loudness_data['std'] = np.std(loudness_store)

	if show_plot==True:
		print('Showing Plot')
		ax = sns.kdeplot(loudness_store,shade=True)
		ax.set(xlabel='dB (Relative Scale)', ylabel='Relative Density', title='Spotify Wrapped 2019 Loudness Data')
		plt.show()
	else:
		pass
		# dont show distribution - for example running on server

	return loudness_data

def tempo_analysis(tracks,auth_header,show_plot=False):

	tempo_store = []

	for track in tracks:
		analysis = get_track_data(track['id'],auth_header)
		tempo_store.append(analysis['tempo'])

	tempo_data = {'average':None,
					 'median':None,
					 'std':None}

	tempo_data['average'] = np.average(tempo_store)
	tempo_data['median'] = np.median(tempo_store)
	tempo_data['std'] = np.std(tempo_store)

	if show_plot==True:
		print('Showing Plot')
		ax = sns.kdeplot(tempo_store,shade=True)
		ax.set(xlabel='Tempo (bpm)', ylabel='Relative Density', title='Spotify Wrapped 2019 Tempo Data')
		plt.show()
	else:
		pass
		# dont show distribution - for example running on server

	return tempo_data

def int_to_key(key_int):

	if key_int == 0:
		key = 'C'
	elif key_int == 1:
		key = 'C#'
	elif key_int == 2:
		key = 'D'
	elif key_int == 3:
		key = 'D#'
	elif key_int == 4:
		key = 'E'
	elif key_int == 5:
		key = 'F'
	elif key_int == 6:
		key = 'F#'
	elif key_int == 7:
		key = 'G'
	elif key_int == 8:
		key = 'G#'
	elif key_int == 9:
		key = 'A'
	elif key_int == 10 or key_int == 't':
		key = 'A#'
	elif key_int == 11 or key_int == 'e':
		key = 'B'
	else:
		key = 'no_key'

	return key

def int_to_mode(mode_int):

	if mode_int == 0:
		mode = 'Minor'
	elif mode_int == 1:
		mode = 'Major'
	else:
		mode = 'No Mode'

	return mode


def key_analysis(tracks,auth_header,show_plot=False):

	key_int_store = []
	mode_int_store = []

	key_dist = {'A':0,
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

	mode_dist = {'Major':0,
				 'Minor':0}

	# Gather data on all of the tracks 
	for track in tracks:
		analysis = get_track_data(track['id'],auth_header)
		key_int_store.append(analysis['key'])
		mode_int_store.append(analysis['mode'])

	# convert the pitch integer notation to actual pitches/keys
	for key_int in key_int_store:
		key = int_to_key(key_int)
		key_dist[key] += 1

	# convert mode integer notation to actual major/mior
	for mode_int in mode_int_store:
		mode = int_to_mode(mode_int)
		mode_dist[mode] += 1

	# Create DataFrame objects from the dictionary of distributions
	df_keys = pd.DataFrame(key_dist,index=[0])
	df_mode = pd.DataFrame(mode_dist,index=[0])

	if show_plot == True:
		# Plot as a bar 
		plt.figure(1)
		plt.bar(x=range(len(key_dist)),height=list(key_dist.values()),align='center',color='teal')
		plt.xticks(ticks=range(len(key_dist)), labels=list(key_dist.keys()))
		plt.xlabel('Key')
		plt.ylabel('Count')
		plt.title('Spotify Wrapped 2019 Key Distribution')
		#print(key_dist.keys())
		plt.figure(2)
		plt.bar(x=range(len(mode_dist)),height=list(mode_dist.values()),align='center',color='teal')
		plt.xticks(ticks=range(len(mode_dist)), labels=list(mode_dist.keys()))
		plt.xlabel('Mode')
		plt.ylabel('Count')
		plt.title('Spotify Wrapped 2019 Mode Distribution')
		#print(mode_dist.keys())

		plt.show()

	return key_dist, mode_dist

if __name__ == '__main__':

	spotify_authenticator = Authenticator('testing/configs/config.ini')
	spotify_authenticator.authorize()
	auth_header = spotify_authenticator.generate_header()

	username = 'NLeRoy917'
	wrapped_2019 = 'https://open.spotify.com/playlist/37i9dQZF1Ethb70Ir9WW6o?si=yrv4GDu6SBeUc8PexoZ_HQ'

	playlist_id = get_playlist_id(wrapped_2019)

	tracks = get_tracks(playlist_id,auth_header)

	for track in tracks:
		analysis = get_track_data(track['id'],auth_header)
		print(track['name'],'|',analysis['loudness'])


