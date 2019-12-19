# SpottyData.com API

This is the back-end web API for the website www.SpottyData.com. Built with Flask, it acts as the interface between the site and Spotify's official API. Here you can find the code for the API, End-Point Documentation, or rasie any issues/comments! The base URL is: `https://api.spottydata.com/v1/`

# Endpoints

## User Data

| Method | Endpoint                              | Usage                              | Returns                                 | Resources   |
|--------|---------------------------------------|------------------------------------|-----------------------------------------|-------------|
| GET    | /v1/{user_id}                         | Get a user's profile information   | User Object                             | Spotify API |
| GET    | /v1/{user_id}/playlists               | Get a users playlists              | List of minimal playlist objects        | Spotify API |
| GET    | /v1/{user_id}/playlists/{playlist_id} | Get a specific playlist            | List of playlist objects                | Spotify API |
| GET    | /v1/{user_id}/top/{type}              | Get a users top artists and tracks | List of artist objects or track objects | Spotify API |
### api.domain/test/
    Test URL - Returns string "Thor is the Strongest Avenger"

### api.domain/user/playlists/
    Returns list of a users playlists
    #### Methods: GET
    #### Header Fields: access_token - users access token which has been aquired with the appropriate scope (https://developer.spotify.com/documentation/general/guides/authorization-guide/#list-of-scopes)
   
