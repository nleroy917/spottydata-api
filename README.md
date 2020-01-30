# SpottyData.com API

This is the back-end web API for the website www.SpottyData.com. Built with Flask, it acts as the interface between the site and Spotify's official API. Here you can find the code for the API, End-Point Documentation, or rasie any issues/comments! The base URL is: `https://spottydata-api.herokuapp.com/`

# Endpoints
### User Data

| Method | Endpoint                              | Usage                              | Returns                                 | Resources   |
|--------|---------------------------------------|------------------------------------|-----------------------------------------|-------------|
| GET    | /{user_id}                         | Get a user's profile information   | User Object                             | Spotify API |
| GET    | /{user_id}/playlists               | Get a users playlists              | List of minimal playlist objects        | Spotify API |
| GET    | /{user_id}/playlists/{playlist_id} | Get a specific playlist            | List of playlist objects                | Spotify API |
| GET    | /{user_id}/top/{type}              | Get a users top artists and tracks | List of artist objects or track objects | Spotify API |

### Playlist Analysis
| Method | Endpoint                     | Usage                                       | Returns                                        | Resources                             |
|--------|------------------------------|---------------------------------------------|------------------------------------------------|---------------------------------------|
| POST   | /analysis/lyrics          | Analyze song lyrics in playlist             | List of lyrics objects                                | Spotify API, Genius API, Google Cloud |
| POST   | /analysis/audio/{feature} | Analyze playlist for certain audio feature  | List of raw data for the audio feature to plot | Spotify API                           |

   
