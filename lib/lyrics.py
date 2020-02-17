import os
import sys
sys.path.append('..')


from dotenv import load_dotenv
load_dotenv()

# import custom libraries
from lib.authorize import *
from lib.playlists import *

import time
import string
from configparser import SafeConfigParser
import numpy as np
import lyricsgenius

def get_lyrics(track,GENIUS_API_SECRET):

	genius = lyricsgenius.Genius(GENIUS_API_SECRET)

	try:
		song = genius.search_song(track['name'], track['artists'][0]['name'])
	except:
		pass

	if song:
		return song.lyrics
	else:
		return None


def parse_lyrics(lyrics):

	lines = lyrics.split('\n')
	translator = str.maketrans('', '', string.punctuation)
	words_list = []

	for line in lines:
		if '[' in line or ']' in line:
			continue
		#print(line)
		cleaned_line = line.translate(translator)
		#print(cleaned_line)
		#time.sleep(0.5)

		words = cleaned_line.split(' ')
		for word in words:
			if word == '':
				continue
			if 'u\2005' in word:
				continue
			words_list.append(word)

	return words_list




if __name__ == '__main__':

	GENIUS_API_SECRET=os.getenv('GENIUS_API_SECRET')

	spotify_authenticator = Authenticator('../tests/config.ini')
	spotify_authenticator.authorize()
	auth_header = spotify_authenticator.generate_header()

	playlist_id = '37i9dQZF1Ethb70Ir9WW6o'

	tracks = get_tracks(playlist_id,auth_header)

	cnt = 1

	lyrics_count = {}

	for track in tracks[0:10]:
		print('Track {}/{}'.format(cnt,len(tracks)))
		lyrics = get_lyrics(track,GENIUS_API_SECRET)
		words = parse_lyrics(lyrics)

		for word in words:
			if word in lyrics_count:
				lyrics_count[word.capitalize()] += 1
			else:
				lyrics_count[word.capitalize()] = 1


		cnt += 1
	lyrics_count_sorted = {k: v for k, v in sorted(lyrics_count.items(), key=lambda item: item[1])}
	{0: 0, 2: 1, 1: 2, 4: 3, 3: 4}

	print(lyrics_count_sorted)






