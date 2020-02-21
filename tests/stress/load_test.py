from locust import HttpLocust, TaskSet, task, between

import sys
sys.path.append("..")
sys.path.append("../..")

from lib.authorize import *
from lib.playlists import *
from utils.authentication import *

ACCESS_TOKEN = get_access_token()
PLAYLIST_ID, PLAYLIST_NAME = get_playlist()

class UserBehaviour(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.test()

    def test(self):
        self.client.get('/test',headers={"access_token": ACCESS_TOKEN})

    @task(1)
    def index(self):
        self.client.get("/")

    @task(1)
    def get_tracks(self):
        self.client.get('/playlists/{}/tracks'.format(PLAYLIST_ID), headers={"access_token": ACCESS_TOKEN})

class WebsiteUser(HttpLocust):
    task_set = UserBehaviour
    wait_time = between(5, 9)