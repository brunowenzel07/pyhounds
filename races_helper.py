# -*- coding: UTF-8
# !/usr/bin/python 
import numpy as np 
import re 

class RaceHelper:

    def __init__(self, content):

        def normalize_text(txt):
            return txt.text.encode("utf-8")

        self.content = {
            "distance" : normalize_text(content[2]),
            "split" : normalize_text(content[4]),
            "bends" : normalize_text(content[5]),
            "fin" : normalize_text(content[6]),
            "remarks" : normalize_text(content[9]).split(","),
            "winner_time": normalize_text(content[10]),
            "gng" : normalize_text(content[11]),
            "wght" : normalize_text(content[12]),
            "cal_time" : normalize_text(content[15]),
        }

    def distance(self):
        return int(self.content["distance"].replace("m", ""))

    def split(self):
        return float(self.content["split"])
    
    def bends(self):
        bends = np.array(list(self.content["bends"])).astype(np.float)
        df1 = (bends[0] - bends[1])/2
        df2 = (bends[2] - bends[3])/2
        df3 = (int(re.sub("\D", "", self.content["fin"])) - bends[0])/2
        return round((df1-df2-df3)/3, 2)

    def finished(self):
        return int(re.sub("\D", "", self.content["fin"]))

    def remarks(self):
        return self.content["remarks"]

    def winner_time(self):
        return float(self.content["winner_time"])

    def calculate_time(self):
        return float(self.content["cal_time"])

    def weight(self):
        return float(self.content["wght"])

    def array_data(self):
        result = [
            self.distance(),
            self.split(),
            self.bends(),            
            self.remarks(),            
            self.calculate_time(),
            self.winner_time(),
            self.weight(),
            self.finished(),
        ]
        return result 