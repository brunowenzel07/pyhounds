from selenium import webdriver 
import click 
from database import Database

import sys 
sys.path.insert(0, "functions/")
from tracks import Tracks
from dogs import Dogs
import numpy as np 
from helper import Helper

def run(url):
    driver = webdriver.Chrome()
    tracks = Tracks(url, driver)
    dogs = Dogs()
    helper = Helper()
    db = Database("data/data_train.csv")
    for track in tracks.get_tracks():
        page_html = helper.get_page_code("http://greyhoundbet.racingpost.com/%s" % track, driver, type_wait="class", element_wait="meetingResultsList")
        for dog in dogs.get_dogs(page_html, "meetings"):
            stat = dogs.get_stats(dog)
            break 
        break 
    driver.close()