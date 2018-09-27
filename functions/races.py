# -*- coding: UTF-8
# !/usr/bin/python 
import numpy as np 
import re
import nltk
import pandas as pd
import csv 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from string import digits 

class Race:

    def __init__(self, content):

        def normalize_text(txt):
            return txt.text.encode("utf-8")
        self.content = {
            "distance" : normalize_text(content[2]),
            "trap" : normalize_text(content[3]),
            "split" : normalize_text(content[4]),
            "bends" : normalize_text(content[5]),
            "fin" : normalize_text(content[6]),
            "remarks" : normalize_text(content[9]),
            "winner_time": normalize_text(content[10]),
            "gng" : normalize_text(content[11]),
            "wght" : normalize_text(content[12]),
            "sp" : normalize_text(content[13]),
            "cal_time" : normalize_text(content[15]),
        }

    def normalize_stats(self):

        def distance():
            return int(self.content["distance"].replace("m", ""))
    
        def bends():
            bends = np.array(list(self.content["bends"])).astype(np.float)
            return bends

        def trap():
            trap = int(self.content["trap"].replace("[", "").replace("]", ""))
            return trap

        def split():
            return float(self.content["split"])

        def remarks():
            
            return self.content["remarks"].replace(
                "/", " ").replace(
                "&", " ").replace(
                ",", " ").replace(
                "-", " ").translate(None, digits)

        def winner_time():
            return float(self.content["winner_time"])
        
        def gng():
            gng = self.content["gng"]
            if gng == "N": return 0
            else: return float(gng)

        def weight():
            return float(self.content["wght"])

        def calc_time():
            return float(self.content["cal_time"])

        def sp():
            sp = self.content["sp"]
            sp = sp.split("/")
            x = lambda a : float(re.sub("\D", "", a))
            nom = x(sp[0])
            den = x(sp[1])
            return round(nom/den, 3)

        def fin():
            d = re.search("\d", self.content["fin"])            
            return int(d.group())

        result = [
            distance(),
            bends(),       
            trap(),
            remarks(), 
            gng(),
            calc_time(),
            sp(),
            split(),
            weight(),
            winner_time(),
            fin()
        ]
        return result 
    
    def calculate_stats(self, content, clf, bow, tfidf):     

        def bends():
            diff = content[1][0] - content[-1]
            if diff > 0: return 1
            elif diff < 0: return -1
            else: return 0
        
        def remarks():
            X_bow = bow.transform([content[3]])            
            X_tfidf = tfidf.transform(X_bow)   
            pred = clf.predict(X_tfidf)         
            return int(pred)

        def finishes():
            if int(content[-1]) > 2 : return 1
            else: return 0
            print(int(content[-1]))

        def gng():
            if content[4] < 0: return -1
            elif content[4] > 0: return 1 
            else: return 0
        
        def sp():
            return content[6]

        def trap():
            return content[2]
        
        def weight():
            return content[8]

        def split():
            return float(content[0])/content[7]

        try: 
            result = [
                bends(),
                remarks(),
                finishes(),
                gng(),
                sp(),
                trap(),
                weight(),
                split()
            ]
        except Exception:
            result = []
        return result 