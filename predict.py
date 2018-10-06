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
import csv 
from datetime import datetime 
import Queue
import threading 
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.preprocessing import Normalizer

chrome_options = webdriver.ChromeOptions()
prefs={
    "profile.managed_default_content_settings.images": 2, 
    "profile.managed_default_content_settings.stylesheet": 2, 
    'disk-cache-size': 8192 
    }
chrome_options.add_experimental_option('prefs', prefs)

def run():   
    
    db = Database("data/data_train.csv")
    db2 = Database("predicts/predicts.csv")
    data_train = db.load()
    data_test = db.load_tuning()
    scaler = Normalizer()
    X_scaler = scaler.fit_transform(data_train[0])
    clf = LinearDiscriminantAnalysis()
    clf.fit(X_scaler, data_train[1])

    
    # Get tracks for URL 
    tracks = Tracks(type_track="predicts")

    # Instance of dogs
    dogs, helper = Dogs(), Helper()

    # Create a instance for remarks classifier    
    remarks_clf = helper.remarks_clf()

    url_date = datetime.now()

    # Create a instance for webdriver 
    driver = webdriver.Chrome(chrome_options=chrome_options)

    for track in tracks.get_tracks():

        print("Getting data from: %s" % track)

        # Get page of track 
        page_html = helper.get_page_code(track[3], driver, type_wait="class", element_wait="runnerBlock")        

        with click.progressbar(dogs.get_dogs(page_html, "predicts")) as bar2:
            # create a queue
            q = Queue.Queue()
            # Iterate about dogs in page
            for dog in bar2:
                # Receive dog_page 
                dog_page = dogs.get_page(dog,driver)

                # Auxiliary array 
                whelping, last_run = helper.get_dog_dates(dog_page, url_date)
                print(whelping, last_run)
                thread1 = threading.Thread(target=dogs.get_stats, args=[dog, dog_page, remarks_clf, "predict", q, url_date, whelping, last_run])
                thread1.start()
                
        thread1.join()
        preds = []
        while not q.empty():
            stat = q.get()
            if len(stat) > 0:
                pred = round(clf.predict_proba(scaler.fit_transform([stat]))[0][0], 2)
                preds.append(pred)
        if len(preds) == 6:
            row = track[:3] + preds
            db2.insert(row, "solo")
    driver.close()
