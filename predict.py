# -*- coding: UTF-8
# !usr/bin/python 
from selenium import webdriver 
import click 
from database import Database
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import Normalizer
import sys 
sys.path.insert(0, "functions/")
from dogs import Dogs
import numpy as np 
import pandas as pd 
from helper import Helper 

def run(url):
    driver = webdriver.Chrome()
    dogs = Dogs()    

    db = Database("data/data_train.csv")
    data_train = db.load()    
    normalize = Normalizer()
    helper = Helper()
    clf = KNeighborsClassifier(n_neighbors=2, p=3)
    data_train_scaled = normalize.fit_transform(data_train[0])
    clf.fit(data_train_scaled, data_train[1])
 
    probas, names, traps, preds = [], [], [], []
    page_html = helper.get_page_code(url, driver, type_wait="class", element_wait="runnerBlock")

    location = page_html.find("div", class_="pageHeader").find("h2").text.encode("utf-8")
    race = page_html.find("span", {"id":"title-circle-container"}).find("span", class_="titleColumn1").text.encode("utf-8")
    post_tip = page_html.find("span", {"id":"title-circle-container"}).find("p", class_="p2").text.encode("utf-8")[2:-1]
    dogs_race = dogs.get_dogs(page_html, "cards")
    for dog in dogs_race:
        sample = dogs.get_stats(dog, driver, "card") 
        if len(sample) > 0:
            sample_scaled = normalize.fit_transform([sample[:-1]])
            pred = int(clf.predict(sample_scaled))
            pred_proba = clf.predict_proba(sample_scaled)
            probas.append("/".join(map(str,pred_proba[0])))
            if pred == 0: preds.append("Place")         
            if pred == 1: preds.append("Not Place")         
            names.append(dog[1])         
            traps.append(dog[3])   

    frame = {
        "Trap" : traps,
        "Dog" : names,
        "Predict" : preds,
        "Probability": probas
    }

    df = pd.DataFrame(data=frame)
    click.clear()
    click.secho("   Track: %s" % location, bold=True)
    click.secho("   %s" % race, bold=True)
    click.secho("   %s" % post_tip, bold=True)
    print("     "+df[["Trap", "Dog", "Predict", "Probability"]].sort_values(by="Predict", ascending=False).to_string(index=False))
