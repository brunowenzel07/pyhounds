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
from helper import Helper

dogs = Dogs()
helper = Helper()


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
dog_age = page_html.find("table",class_="pedigree").find_all("td")[3]
last_run = page_html.find("table", {"id":"sortableTable"}).find_all("td", class_="c0")[1]

last_run = helper.normalize(last_run, "date_diff") # last_run muda para train e predict
dog_age = helper.normalize(dog_age, "date_diff")

i = 0
for tr_content in page_html.find("table", {"id":"sortableTable"}).find_all("tr", class_="row"):
    try: 
        race = Race(tr_content.find_all("td"), dog_trap)
        cu = race.calculate_stats(race.normalize_stats(), nb, bow, tfidf)
        if cu[5]:
            dog_races.append(cu)
            i += 1 
    except Exception as a :
        pass
    if i == 5: break 

df = pd.DataFrame(data=dog_races, columns=["bends", "remarks", "finishes", "gng","sp","trap","weight","split"])

result = {
    # Idade do cachorro (em dias)
    "dog_age": int(dog_age),
    # Dias desde a última corrida
    "last_run" : int(last_run),
    # Média da troca de posições nas últimas 5 corridas
    "bends": df["bends"].mean(),
    # Comentários positivos para os últimas corridas
    "remarks" : helper.count_unique(df["remarks"].tolist(), 0),
    # Top 1
    "top_1" : helper.count_unique(df["finishes"].tolist(), 1),
    # Top 2
    "top_2" : helper.count_unique(df["finishes"].tolist(), 1) + helper.count_unique(df["finishes"].tolist(), 2),
    # Top 3
    "top_3" : helper.count_unique(df["finishes"].tolist(), 1) + helper.count_unique(df["finishes"].tolist(), 2) + helper.count_unique(df["finishes"].tolist(), 3),
    # gng avg
    "gng" : df["gng"].mean(),
    # Weight
    "weight" : df["weight"][0],
    # split
    "split" : df["split"].mean()
}

print(df)
print(result)
print(result.values())
