from selenium import webdriver 
import click 
from database import Database

import sys 
sys.path.insert(0, "functions/")
from tracks import Tracks
from dogs import Dogs
import numpy as np 

def run(url):
    driver = webdriver.Chrome()
    tracks = Tracks(url, driver)
    dogs = Dogs()
    db = Database("data/data_train.csv")
    dogs_tracks_urls = tracks.get_tracks()
    print(len(dogs_tracks_urls))
    with click.progressbar(dogs_tracks_urls, length=len(dogs_tracks_urls)) as bar:
        for track in bar:
            dogs_stats = []
            dogs_track = dogs.get_dogs(track, driver)        
            for dog in dogs_track:
                dog_stat = dogs.get_stats(dog, driver)
                if not np.isnan(dog_stat).any() and len(dog_stat) > 0:
                    dogs_stats.append(dog_stat)
            db.insert(dogs_stats)
    driver.close()