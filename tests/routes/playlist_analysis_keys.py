import requests
import json

def test(BASE_URL,access_token,playlist_id):

	headers = {'access_token': access_token}

	r = requests.get(BASE_URL + playlist_id + '/analysis/keys',headers=headers)

	if r.status_code == 200:
		print('\tPASS')
		#print(r.json)
		return True
	else:
		print('\tFAIL',end='')
		print(' | error: {}, {}'.format(r.status_code,r.text))
		return False


if __name__ == '__main__':
	test(access_token,playlist_id)