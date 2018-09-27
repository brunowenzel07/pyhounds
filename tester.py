# -*- coding: UTF-8
# !/usr/bin/python
from bs4 import BeautifulSoup
import sys 
sys.path.insert(0, "functions/")
from dogs import Dogs
from races import Race
import pandas as pd 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report 
import numpy as np 

dogs = Dogs()

with open("html_files/race.html", "r") as html_page:
    page_html = BeautifulSoup(html_page, "html.parser")


train_df = pd.read_csv("data/comments.csv", header=None, names=["comment", "position"])
# Bag of Words
tfidf = TfidfTransformer()
bow = CountVectorizer()
bow.fit(train_df["comment"])
# instanciando classificador
nb = MultinomialNB(alpha=1.0)
# treinamento, transformação do set de trainamento
train_X_bow = bow.transform(train_df["comment"])
tfidf.fit(train_X_bow)
train_X_tfidf = tfidf.transform(train_X_bow)
train_y = train_df["position"]
nb.fit(train_X_tfidf, train_y)

dog_races = []

dog_trap = int(page_html.find("h1", class_="ghName").find("i").attrs["class"][1].replace("trap", "").encode("utf-8"))

for tr_content in page_html.find("table", {"id":"sortableTable"}).find_all("tr", class_="row"):
    try: 
        race = Race(tr_content.find_all("td"), dog_trap)
        dog_races.append(race.calculate_stats(race.normalize_stats(), nb, bow, tfidf))
    except Exception as a :
        pass

df = pd.DataFrame(data=dog_races, columns=["bends", "remarks", "finishes", "gng","sp","trap","weight","split"])

result = [round(df[a].mean(), 3) for a in df]

print(result)