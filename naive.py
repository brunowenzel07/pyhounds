# -* coding: UTF-8
#! /usr/bin/python 

import pandas as pd 
import numpy as np 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report 

# Importa os dados para treino
train_df = pd.read_csv("data/comments.csv", header=None, names=["comment", "position"])
test_df = pd.read_csv("data/comments_test.csv", header=None, names=["comment", "position"])

# Bag of Words
tfidf = TfidfTransformer()
bow = CountVectorizer()
bow.fit(test_df.append(train_df)["comment"])

# instanciando classificador
nb = MultinomialNB(alpha=1.0)

# treinamento, transformação do set de trainamento
train_X_bow = bow.transform(train_df["comment"])
tfidf.fit(train_X_bow)
train_X_tfidf = tfidf.transform(train_X_bow)
train_y = train_df["position"]
nb.fit(train_X_tfidf, train_y)

y_pred = nb.predict(train_X_tfidf)
