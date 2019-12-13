# Spotify Playlist Analyzer Web API
---
This repo holds the code for running and testing the web API version of the spotify playlist analyzer code I originally wrote.

The purpose is to create a front end that can handle authprization, and all that is required is for one to ping this API with the access_token and username, and the routes can then be used to do anaylsis of the data - prefereably in the browser as the data is returned in JSON format...

... In Brief, this API is meant to act as a mediator between the front-end and the spotify API to properly format the data, and run any intermediate analysis required for the data.

# Endpoints
---
### api.domain/
    Base URL - Returns HTML that points user to API documentation
  
### api.domain/test/
    Test URL - Returns string "Thor is the Strongest Avenger"

### api.domain/user/playlists/
    Returns list of a users playlists
    #### Methods: GET
    #### Header Fields: access_token - users access token which has been aquired with the appropriate scope (https://developer.spotify.com/documentation/general/guides/authorization-guide/#list-of-scopes)
   
