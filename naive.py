# -* coding: UTF-8
#! /usr/bin/python 

import pandas as pd 
import numpy as np 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

# Importa os dados para treino
train_df = pd.read_csv("data/comments.csv", header=None, names=["comment", "position"])

# Bag of Words
tfidf = TfidfTransformer()
bow = CountVectorizer()
bow.fit(train_df["comment"])

# treinamento
train_X_bow = bow.transform(train_df["comment"])
tfidf.fit(train_X_bow)
train_X_tfidf = tfidf.transform(train_X_bow)
train_y = train_df["position"]

nb = MultinomialNB(alpha=1.0)
nb.fit(train_X_tfidf, train_y)
y_pred = nb.predict(train_X_tfidf)


print(accuracy_score(train_y, y_pred))
