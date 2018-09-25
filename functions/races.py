# -*- coding: UTF-8
# !/usr/bin/python 
import numpy as np 
import re
import nltk


class Race:

    def __init__(self, content, dog):

        def normalize_text(txt):
            return txt.text.encode("utf-8")
        self.content = {
            "distance" : normalize_text(content[2]),
            "trap" : normalize_text(content[3]),
            "split" : normalize_text(content[4]),
            "bends" : normalize_text(content[5]),
            "fin" : normalize_text(content[6]),
            "remarks" : normalize_text(content[9]).split(","),
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
            return self.content["remarks"]

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

        result = [
            distance(),
            bends(),       
            trap(),
            remarks(), 
            gng(),
            calc_time(),
            sp()
        ]
        return result 
    
    def calculate_stats(self):
        data = self.normalize_stats()
        print(data)

        def bends():
            diff = data[1][0] - data[-1]
            if diff > 0: return 1
            elif diff < 0: return -1
            else: return 0
        
        def remarks():
            remarks = data[3]
            comments = [re.sub("[()\[\]/]", "", i.lower()) for i in remarks]
            print(comments)

        result = [
            bends(),
            remarks()
        ]

        return result