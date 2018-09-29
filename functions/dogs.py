# -*- coding: UTF-8
# !/usr/bin/python 
from helper import Helper
from races import Race
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

class Dogs():

    def __init__(self):
        pass
        self.helper = Helper()
    
    def get_stats(self, dog, driver):
        
        dog_page = self.helper.get_page_code(
            "http://greyhoundbet.racingpost.com/" + dog[2], 
            driver, 
            type_wait="id",
            element_wait="sortableTable")

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

        
        for tr_content in dog_page.find("table", {"id":"sortableTable"}).find_all("tr", class_="row"):
            try: 
                race = Race(tr_content.find_all("td"), dog[3])
                dog_races.append(race.calculate_stats(race.normalize_stats(), nb, bow, tfidf))
            except Exception: pass 
        try: 
            if len(dog_races) > 0:
                df = pd.DataFrame(data=dog_races, columns=[
                    "bends", 
                    "remarks", 
                    "finishes", 
                    "gng",
                    "sp",
                    "trap",
                    "weight",
                    "split"])
                result = [round(df[a].mean(), 3) for a in df]
            else: result = []
        except Exception as a:
            print(a)
            result = []
        return result 


    def get_dogs(self, page_html, type_dogs):
        rows = []
        if type_dogs == "meetings":            
            for dog_div in page_html.find("div", class_="meetingResultsList").find_all("div", class_="container"):
                dog_name = self.helper.normalize(dog_div.find("div", class_="name"), "string")[1:-1]
                dog_place = int(self.helper.normalize(dog_div.find("div", class_="place"), "only_digits"))
                dog_link = self.helper.normalize(dog_div.find("a", class_="details"), "link")                    
                dog_trap = self.helper.normalize(dog_div.find("div", class_="bigTrap"),"trap")
                row =  [ 
                    dog_place,
                    dog_name,
                    dog_link,
                    dog_trap
                ]
                rows.append(row)
        elif type_dogs == "predicts":
            for dog_div in page_html.find("div", class_="cardTabContainer").find_all("div", class_="runnerBlock"):
                dog_name = self.helper.normalize(dog_div.find("a", class_="gh").find("strong"), "string")[1:-1]
                dog_link = self.helper.normalize(dog_div.find("a", class_="gh"), "link")                    
                dog_trap = self.helper.normalize(dog_div.find("i", class_="bigTrap"),"trap")
                dog_comment = self.helper.normalize(dog_div.find("p", class_="comment"),"string")
                row = [dog_name, dog_comment, dog_link, dog_trap]
                rows.append(row)
        return rows
