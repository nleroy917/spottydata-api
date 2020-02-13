# SpottyData.com API

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Heroku](https://heroku-badge.herokuapp.com/?app=spottydata-api)

This is the back-end web API for the website www.SpottyData.com. Built with Flask, it acts as the interface between the site and Spotify's official API. Here you can find the code for the API, End-Point Documentation, or rasie any issues/comments! The base URL is: `https://spottydata-api.herokuapp.com/`

# Endpoints
### User Data

| Method | Endpoint                              | Usage                              | Returns                                 | Resources   |
|--------|---------------------------------------|------------------------------------|-----------------------------------------|-------------|
| GET    | /{user_id}                         | Get a user's profile information   | User Object                             | Spotify API |

### Playlist Analysis
| Method | Endpoint                     | Usage                                       | Returns                                        | Resources                             |
|--------|------------------------------|---------------------------------------------|------------------------------------------------|---------------------------------------|
| POST   | /analysis/lyrics          | Analyze song lyrics in playlist             | List of lyrics objects                                | Spotify API, Genius API, Google Cloud |


   
