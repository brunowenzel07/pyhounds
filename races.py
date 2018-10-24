# -*- coding: UTF-8
# !/usr/bin/python 
import numpy as np 
import re
import nltk
import pandas as pd
import csv 
from string import digits 

class Races:

    def __init__(self, content, dog_trap):
        self.dog_trap = dog_trap 
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
            "grade" : normalize_text(content[14]),
            "cal_time" : normalize_text(content[15]),
        }

    def normalize_stats(self):

        def distance():
            return int(self.content["distance"].replace("m", ""))
    
        def calc_time():
            return float(self.content["cal_time"])

        def fin():
            d = re.search("\d", self.content["fin"])            
            return int(d.group())

        def grade():
            return self.content["grade"]

        result = [
            distance(),                                                   
            calc_time(),
            fin(),
            grade()
        ]
        return result 
    
   