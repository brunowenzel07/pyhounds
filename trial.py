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


clf = KNeighborsClassifier(n_neighbors=2, p=3)
clf.fit(X_scaler, data_train[1])
Y_pred = clf.predict(X_test_scaler)
Y_true = data_test[1]

print(classification_report(Y_true, Y_pred, target_names=["W/P", "Not W/P"]))