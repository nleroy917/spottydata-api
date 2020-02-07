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

	access_token = 'BQC8Ynw7HH2JCtT58q5zRyU7hicU4rIsU562YmwnfkRD7kadXqWS24n1WJUkUDMz62NUUZE3G0k3zz-fsxNmaXWwqvuSSBL0R-pWHXQf25IeyJGsPOm7ar6va-kRVJ4UngIYpcJApeHR6TbJzGWgKYvCXJCg3wVrbkOP3g'
	playlist_id = '2GW9urbbhKa5TsDIthcdPV'

	test(access_token,playlist_id)