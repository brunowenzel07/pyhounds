# -*- coding: UTF-8
# !usr/bin/python 
from selenium import webdriver 
import click 
from database import Database
import sys 
sys.path.insert(0, "functions/")
from dogs import Dogs
import numpy as np 
import pandas as pd 
from helper import Helper 
from os import system 
from tracks import Tracks
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import Normalizer


chrome_options = webdriver.ChromeOptions()
prefs={
    "profile.managed_default_content_settings.images": 2, 
    "profile.managed_default_content_settings.stylesheet": 2, 
    'disk-cache-size': 8192 
    }
chrome_options.add_experimental_option('prefs', prefs)

def run(url):       
    driver = webdriver.Chrome(chrome_options=chrome_options)
    tracks = Tracks(url, False, "predicts")
    dogs = Dogs()
    helper = Helper()
    db = Database("data/data_train.csv")
    data_train = db.load()

    clf = KNeighborsClassifier(n_neighbors=2, p=3)
    clf.fit(data_train[0], data_train[1])

    for race in tracks.get_tracks():
        page_html = helper.get_page_code(race[3], driver, type_wait="class", element_wait="runnerBlock")
        for dog in dogs.get_dogs(page_html, "predicts"):
            stat = dogs.get_stats(dog, driver)
            pred = clf.predict([stat])
            print(pred, dog, race)
            break 
        break 
    driver.close()

#    with click.progressbar(tracks.get_tracks()) as bar:
#        for track in bar:
#            page_html = helper.get_page_code("http://greyhoundbet.racingpost.com/%s" % track, driver, type_wait="class", element_wait="meetingResultsList")
#            for dog in dogs.get_dogs(page_html, "meetings"):
#                stat = dogs.get_stats(dog, driver)
#                if len(stat) > 0:
#                    if int(dog[0]) <= 2: result = 0
#                    else: result = 1
#                    stat.append(result)
#                    db.insert(stat, "solo") 