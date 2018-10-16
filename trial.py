#-*- coding: UTF-8
#!/usr/bin/python 

from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import Normalizer
from sklearn.metrics import classification_report
from database import Database


db = Database("data/data_train.csv")
data_train = db.load()
data_test = db.load_tuning()

scaler = Normalizer()
X_scaler = scaler.fit_transform(data_train[0])
X_test_scaler = scaler.fit_transform(data_test[0])

