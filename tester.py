# -*- coding: UTF-8
# !/usr/bin/python
from bs4 import BeautifulSoup
import sys 
import pprint
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
from datetime import datetime 
dogs = Dogs()
helper = Helper()
import re 


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



i = 0
url = "http://greyhoundbet.racingpost.com/#results-dog/race_id=1580427&dog_id=510397&r_date=2018-01-01&track_id=62&r_time=11:03"
url_date = re.search("r_date=(.+?)&track_id", url)
url_date = datetime.strptime(url_date.group()[7:-9], "%Y-%m-%d")
whelping, last_run = helper.get_dog_dates(page_html, "train", url_date)
remarks_clf = helper.remarks_clf()

for tr_content in page_html.find("table", {"id":"sortableTable"}).find_all("tr", class_="row"):
    try: 
        break 
        tds = tr_content.find_all("td")        
        run_date = datetime.strptime(tds[0].text.encode("utf-8").replace(" ", ""),"%d%b%y")
        
        if run_date < url_date:      
            dog_age_in_run = int((run_date - whelping).days)
            days_until_last_run = last_run
            print(last_run)
            
        
    except Exception as a :
        print(a)

    if i == 5: break 
