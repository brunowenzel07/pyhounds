# -*- coding: UTF-8
# !/usr/bin/python 
from helper import Helper
from races import Races
import pandas as pd
import numpy as np
import re 
from datetime import datetime 

class Dogs():

    def __init__(self):
        pass
        self.helper = Helper()
    
    def get_page(self, dog, driver):
        dog_page = self.helper.get_page_code(
            "http://greyhoundbet.racingpost.com/" + dog[2], 
            driver, 
            type_wait="id",
            element_wait="sortableTable")
        return dog_page 

    def get_stats(self, dog, dog_page, dates, remarks_clf):

        # Define dog trap 
        dog_trap = dog[3]
        dog_races = []
        i = 0
        for tr_content in dog_page.find("table", {"id":"sortableTable"}).find_all("tr", class_="row"):            
            try: 
                tds = tr_content.find_all("td")
                run_date_tr = datetime.strptime(tds[0].text.encode("utf-8").replace(" ", ""),"%d%b%y")                
                if run_date_tr < dates[2]:
                    dog_age = self.helper.normalize(dog_page.find("table",class_="pedigree").find_all("td")[3], "date")
                    race = Races(tds, dog[3])
                    race_data = race.calculate_stats(race.normalize_stats(), remarks_clf)
                    if race_data[6]:
                        dog_races.append(race_data)
                    i += 1 
            except Exception as a :
                print(a)
        dog_stats = pd.DataFrame(data=dog_races, columns=["distance","bends", "remarks", "finishes", "gng","sp","trap","weight","split", "ratio"])    
        
        df = dog_stats.head()

        print(df)

        # Bends -> Max position variation
        bends = df["bends"].std()
        split = df["split"].mean()
        ratio = df["ratio"].mean()
        remarks = 1 - df["remarks"].mean()
        finishes = df["finishes"].mean()
        print(bends, split/ratio, remarks, finishes)

        return []

    def get_dogs(self, page_html, type_dogs, a=False, b=False):
        rows = []
        if type_dogs == "meetings":            
            for dog_div in page_html.find("div", class_="meetingResultsList").find_all("div", class_="container"):
                dog_name = self.helper.normalize(dog_div.find("div", class_="name"), "string")[1:-1]
                dog_place = int(self.helper.normalize(dog_div.find("div", class_="place"), "only_digits"))
                dog_link = self.helper.normalize(dog_div.find("a", class_="details"), "link")                    
                dog_trap = self.helper.normalize(dog_div.find("div", class_="bigTrap"),"trap")
                if dog_place <= 3:
                    dog_place = 0
                else: 
                    dog_place = 1
                row =  [ 
                    dog_place,
                    dog_name,
                    dog_link,
                    dog_trap
                ]
                rows.append(row)
        elif type_dogs == "predicts":
            for dog_div in page_html.find("div", class_="cardTabContainer").find_all("div", class_="runnerBlock"):
                dog_trap = self.helper.normalize(dog_div.find("i", class_="bigTrap"),"trap")
                if dog_trap in [a,b]:
                    dog_name = self.helper.normalize(dog_div.find("a", class_="gh").find("strong"), "string")[1:-1]
                    dog_link = self.helper.normalize(dog_div.find("a", class_="gh"), "link")                                    
                    dog_comment = self.helper.normalize(dog_div.find("p", class_="comment"),"string")
                    row = [dog_name, dog_comment, dog_link, dog_trap]
                    rows.append(row)
        return rows