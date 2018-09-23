# -*- coding: UTF-8
# !/usr/bin/python 
import click 
from database import Database

import sys 
sys.path.insert(0, "functions/")
from tracks import Tracks
from dogs import Dogs


from sklearn.preprocessing import Normalizer
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import classification_report
from sklearn.neighbors import KNeighborsClassifier
from selenium import webdriver

def run(url):
    dogs = Dogs()

    db = Database("data/data_train.csv")
    data_test = db.load_tuning()
    data_train = db.load()    

    normalize = Normalizer()

    #clf = KNeighborsClassifier(n_neighbors=15, p=3)
    clf = AdaBoostClassifier()

    data_train_scaled = normalize.fit_transform(data_train[0])

    clf.fit(data_train_scaled, data_train[1])
    
    i, k = 0., 0.
    Y_pred, Y_true = [], []
    for sample in data_test:
        sample_scaled = normalize.fit_transform([sample[:-1]])
        Y_pred.append(int(clf.predict(sample_scaled)))
        Y_true.append(int(sample[-1]))
        
    print(classification_report(Y_true, Y_pred, target_names={"Place", "Not Place"}))