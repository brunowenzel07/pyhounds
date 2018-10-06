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

def run(url):   
    
    db = Database("data/data_train.csv")
    db2 = Database("predicts/predicts.csv")
    data_train = db.load()
    data_test = db.load_tuning()
    scaler = Normalizer()
    X_scaler = scaler.fit_transform(data_train[0])
    clf = LinearDiscriminantAnalysis()
    clf.fit(X_scaler, data_train[1])

    # Instance of dogs
    dogs, helper = Dogs(), Helper()

    # Create a instance for remarks classifier    
    remarks_clf = helper.remarks_clf()

    url_date = datetime.now()

    # Create a instance for webdriver 
    driver = webdriver.Chrome(chrome_options=chrome_options)


    print("Getting data from: %s" % url)

    # Get page of track 
    page_html = helper.get_page_code(url, driver, type_wait="class", element_wait="runnerBlock")        
    
    # create a queue
    q = Queue.Queue()

    # Iterate about dogs in page
    for dog in dogs.get_dogs(page_html, "predicts"):
        # Receive dog_page 
        dog_page = dogs.get_page(dog,driver)
        # Auxiliary array 
        whelping, last_run = helper.get_dog_dates(dog_page, url_date)
        thread1 = threading.Thread(target=dogs.get_stats, args=[dog, dog_page, remarks_clf, "predict", q, url_date, whelping, last_run])
        thread1.start()
            
    thread1.join()
    stats = []
    while not q.empty():
        stat = q.get()        
        if len(stat) > 0:
            stats.append(stat)   

    a = 2
    b = 3
    for i, s in enumerate(stats):
        for k, t in enumerate(stats):
            try: 
                a_position = int(s[-1])
                b_position = int(t[-1])
                if a_position != b_position:                    
                    if a_position == a and b_position == b:                        
                        row = s[:-1] + t[:-1]
                        pred = clf.predict(scaler.fit_transform([row]))
                        print(pred)
            except Exception as a:
                pass
    driver.close()
