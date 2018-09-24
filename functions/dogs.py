# -*- coding: UTF-8
# !/usr/bin/python 
from helper import Helper
from races import Race
import pandas as pd
import numpy as np

class Dogs():

    def __init__(self):
        pass
        self.helper = Helper()
    
    def get_stats(self, dog, driver, dog_type):
        
        dog_page = self.helper.get_page_code(
            "http://greyhoundbet.racingpost.com/" + dog[2], 
            driver, 
            type_wait="id",
            element_wait="meetingResultsList")

        for dog_div in dog.dog_page.find("div", class_="meetingResultsList").find_all("div", class_="container"):
            

    def get_dogs(self, page_html, type_dogs):
        rows = []
        if type_dogs == "meetings":            
            for dog_div in page_html.find("div", class_="meetingResultsList").find_all("div", class_="container"):
                dog_name = self.helper.normalize(dog_div.find("div", class_="name"), "string")[1:-1]
                dog_place = int(self.helper.normalize(dog_div.find("div", class_="place"), "only_digits"))
                dog_link = self.helper.normalize(dog_div.find("a", class_="details"), "link")                    
                row =  [ 
                    dog_place,
                    dog_name,
                    dog_link,
                ]
                rows.append(row)
        if type_dogs == "cards":
            for dog_div in page_html.find("div",{"id":"sortContainer"}).find_all("div", class_="runnerBlock"):
                try:
                    dog_name = self.helper.normalize(dog_div.find("a", class_="dogName").find("strong"), "string")[1:-1]
                    dog_brt = self.helper.normalize(dog_div.find("td", class_="brt"), "brt")
                    dog_link = self.helper.normalize(dog_div.find("a", class_="dogName"), "link")
                    dog_trap = self.helper.normalize(dog_div.div.find("a", class_="dogName"),"trap")
                    dog = [
                        dog_brt,
                        dog_name,
                        dog_link,
                        dog_trap
                    ]
                    rows.append(dog)
                except Exception:
                    pass
        return rows
