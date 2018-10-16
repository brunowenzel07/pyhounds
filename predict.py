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
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import Normalizer
import time
from googletrans import Translator


chrome_options = webdriver.ChromeOptions()
prefs={
    "profile.managed_default_content_settings.images": 2, 
    "profile.managed_default_content_settings.stylesheet": 2, 
    'disk-cache-size': 8192 
    }
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_argument("--headless")

def run(url, a, b):   
    
    db = Database("data/data_train.csv")
    db2 = Database("predicts/predicts.csv")
    data_train = db.load()
    data_test = db.load_tuning()
    scaler = Normalizer()
    X_scaler = scaler.fit_transform(data_train[0])
    clf = KNeighborsClassifier(n_neighbors=2, p=3)
    clf.fit(X_scaler, data_train[1])

    # Instance of dogs
    dogs, helper = Dogs(), Helper()

    translator = Translator()
    
    # Create a instance for remarks classifier    
    remarks_clf = helper.remarks_clf()

    url_date = datetime.now()

    # Create a instance for webdriver 
    driver = webdriver.Chrome(chrome_options=chrome_options)


    print("Getting data from: %s" % url)

    # Get page of track 
    page_html = helper.get_page_code(url, driver, type_wait="class", element_wait="runnerBlock")        
    
    # Track informations
    track = helper.track_informations(page_html)

    # create a queue
    q = Queue.Queue()

    comments, dogs_names = [], []
    # Iterate about dogs in page
    for dog in dogs.get_dogs(page_html, "predicts", a, b):
        # Receive dog_page 
        dog_page = dogs.get_page(dog,driver)
        # Auxiliary array 
        whelping, last_run = helper.get_dog_dates(dog_page, url_date)
        thread1 = threading.Thread(target=dogs.get_stats, args=[dog, dog_page, remarks_clf, "predict", q, url_date, whelping, last_run])
        thread1.start()
        comments.append(dog[1])
        dogs_names.append(dog[0])
            
    thread1.join()
    stats = []
    while not q.empty():
        stat = q.get()        
        if len(stat) > 0:
            stats.append(stat[:-1])   

    click.clear()

    time.sleep(5)    

    
    if len(stats) != 2:
        print("Sem dados suficientes")
    else:
        scaled_data = scaler.fit_transform([stats[0] + stats[1]])        
        pred = int(clf.predict(scaled_data))
        
        if pred == 1:
            label = "*[%s] %s (v %s [%s])*" % (a, dogs_names[0], dogs_names[1], b)
            comment = "%s (v %s)" % (comments[0], comments[1])
        elif pred==0:
            label = "*[%s] %s (v %s [%s])*" % (b, dogs_names[1], dogs_names[0], a)
            comment = "%s (v %s)" % (comments[1], comments[0])

        
        output = "*{} - {}* \n{} \n{} \n".format(track[1], track[0], label, comment)

        print(output)


    driver.close()
