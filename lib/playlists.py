from lib.authorize import *
from configparser import SafeConfigParser

def get_playlist_id(share_url):

    id = share_url[share_url.find('playlist/') + len('playlist/'):share_url.find('?')]

    return id

def get_playlists(user,auth_header):
    response = requests.get('https://api.spotify.com/v1/users/{}/playlists'.format(user),
                            headers=auth_header)

    return_package = json.loads(response.text)
    playlists = return_package['items']

    return playlists

def add_to_playlist(playlist_id,track_uris,auth_header):

    auth_header['Content-Type'] = 'application/json'

    body = {'uris':track_uris
            }

    #print(body)
    #print(json.dumps(body))

    response = requests.post('https://api.spotify.com/v1/playlists/{}/tracks'.format(playlist_id),
                             data=json.dumps(body),
                             headers=auth_header)



    return True

def get_tracks(playlist_id,auth_header):

    response = requests.get('https://api.spotify.com/v1/playlists/{}/tracks'.format(playlist_id),
                            headers=auth_header)

    tracks = json.loads(response.text)

    #print(tracks)

    parsed_playlist = [x['track'] for x in tracks['items']]

    return parsed_playlist

if __name__ == '__main__':

        playlist_URI = 'spotify:playlist:7iGY7WPiTvvSTr6ZgO3rR2'
        playlist_share_link = 'https://open.spotify.com/playlist/7iGY7WPiTvvSTr6ZgO3rR2?si=iDvebMC4Q8Kderz6HyegOA'
        track_URIs = ['spotify:track:6fTt0CH2t0mdeB2N9XFG5r']
        print(track_URIs)
        spotify_authenticator = Authenticator('configs/config.ini')
        spotify_authenticator.authorize()
        auth_header = spotify_authenticator.generate_header()

        playlist_id = get_playlist_id(playlist_share_link)

        add_to_playlist(playlist_id,track_URIs,auth_header)

        tracks = get_tracks(playlist_id,auth_header)

        for track in tracks:
            print(track['name'],'|',track)
