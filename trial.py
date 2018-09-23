# -*- coding: UTF-*
import numpy as np 
from random import randint
import math 
from sklearn.tree import DecisionTreeRegressor
import click 
X_train = []
Y_train = []

with click.progressbar(range(100000)) as bar:
    for i in bar:
        a = randint(1,50)
        b = randint(1,100)
        c = randint(1,50)
        y = a + b + c
        X_train.append([a] + [b] + [c])
        Y_train.append(y)

clf = DecisionTreeRegressor()
clf.fit(X_train, Y_train)

for i in range(50):
    ai = randint(1,50)
    bi = randint(1,100)
    ci = randint(1,50)
    pred = float(clf.predict([[ai,bi,ci]]))
    true = ai + bi + ci
    print(true, pred)