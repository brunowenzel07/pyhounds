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
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.preprocessing import Normalizer
import csv 

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
    db2 = Database("predicts/predicts.csv")
    data_train = db.load()
    scaler = Normalizer()

    X_data_scaled = scaler.fit_transform(data_train[0])

    clf = LinearDiscriminantAnalysis()
    clf.fit(X_data_scaled, data_train[1])

    with click.progressbar(tracks.get_tracks()) as bar:
        for l, race in enumerate(bar):
            page_html = helper.get_page_code(race[3], driver, type_wait="class", element_wait="runnerBlock")
            preds = []
            for dog in dogs.get_dogs(page_html, "predicts"):
                try:
                    stat = dogs.get_stats(dog, driver)
                    pred = clf.predict_proba(scaler.fit_transform([stat[:-1]]))[0]
                    preds.append(round(pred[0]*100, 2))
                except Exception as a:
                    print(a)

            if len(preds) == 6:
                row = race[:3] + preds                
                with open("predicts/predicts.csv", "a") as short_file:
                    writer1 = csv.writer(short_file)
                    writer1.writerow(row)           

    driver.close()

