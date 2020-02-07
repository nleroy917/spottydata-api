import numpy as np
import sys
sys.path.append("..")

from routes import base
from routes import playlist_analysis_keys
from lib.authorize import *
from lib.playlists import *

def get_access_token():

	spotify_authenticator = Authenticator('config.ini')
	spotify_authenticator.authorize()

	return spotify_authenticator.tokens['access_token']

def get_playlist():

	spotify_authenticator = Authenticator('config.ini')
	spotify_authenticator.authorize()
	auth_header = spotify_authenticator.generate_header()

	playlists = get_playlists(spotify_authenticator.username,auth_header)

	return np.random.choice(playlists)['id']


if __name__ == '__main__':

	ACCESS_TOKEN = get_access_token()
	PLAYLIST_ID = get_playlist()

	print('Running Tests:')
	print('-='*40)

	num_tests = 9
	cnt = 1

	# Test main route
	print('Test (1/{}) | /'.format(num_tests),end='')
	base.test()
	cnt += 1

	# Test key data generation
	print('Test (2/{}) | <playlist_id>/analysis/keys'.format(num_tests),end='')
	playlist_analysis_keys.test(ACCESS_TOKEN,PLAYLIST_ID)
	cnt += 1

