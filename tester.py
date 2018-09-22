# -*- coding: UTF-8
# !/usr/bin/python 
from selenium import webdriver 
import click 
from database import Database

import sys 
sys.path.insert(0, "functions/")
from tracks import Tracks
from dogs import Dogs

def run(url):
    driver = webdriver.Chrome()
    tracks = Tracks(url, driver)
    dogs = Dogs()
    for track in tracks.get_tracks():
        dogs_track = dogs.get_dogs(track, driver)
        for dog in dogs_track:
            dog_stat = dogs.get_stats(dog, driver)
            break 
        break 
    driver.close()