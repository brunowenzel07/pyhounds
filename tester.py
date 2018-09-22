# -*- coding: UTF-8
# !/usr/bin/python 
import click 
from database import Database

import sys 
sys.path.insert(0, "functions/")
from tracks import Tracks
from dogs import Dogs


from sklearn.preprocessing import Normalizer
from sklearn.neighbors import KNeighborsClassifier

def run(url):
    dogs = Dogs()

    db = Database("data/data_train.csv")
    data_test = db.load_tuning()
    data_train = db.load()    

    normalize = Normalizer()

    clf = KNeighborsClassifier(n_neighbors=2,p=3)

    data_train_scaled = normalize.fit_transform(data_train[0])

    clf.fit(data_train_scaled, data_train[1])
    
    i, k = 0., 0.
    for sample in data_test:
        sample_scaled = normalize.fit_transform([sample[:-1]])
        pred = int(clf.predict(sample_scaled))
        result = int(sample[-1])
        print(pred, result)

        if pred == result:
            i += 1 
        k += 1 

    print(i/k)