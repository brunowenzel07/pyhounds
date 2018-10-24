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

    def get_stats(self, dog, dog_page, dates, track):

        # Define dog trap 
        dog_trap = dog[3]
        dog_races = []
        i = 0
      # Define dog trap 
        dog_trap = dog[3]
        stats = []
        for tr_content in dog_page.find("table", {"id":"sortableTable"}).find_all("tr", class_="row"):            
            if i == 5: break 
            tds = tr_content.find_all("td")
            run_date_tr = datetime.strptime(tds[0].text.encode("utf-8").replace(" ", ""),"%d%b%y")                
            if run_date_tr < dates[2]:
                dog_age = self.helper.normalize(dog_page.find("table",class_="pedigree").find_all("td")[3], "date")
                race = Races(tds, dog[3])
                try:
                    race_data = race.normalize_stats()
                    stats.append(race_data)
                except Exception as a:
                    pass

        df = pd.DataFrame(data=stats, columns=[
            "Distances",
            "CalcTime",
            "Position",
            "Grade"
        ])
        df = df.loc[df["Distances"] == int(track[0])]
        categorical = df.loc[df["Grade"] == track[1]]
        old_losing_track, losing_track = 0, 0
        losing_cat, old_losing_cat = 0, 0
        reg_tck, reg_cat = [1], [1]
        for h in df["Position"]:
            if h != 1: 
                losing_track = losing_track + 1
            else: 
                reg_tck.append(losing_track)
                losing_track = 0

        for k in categorical["Position"]:
            if k != 1: 
                losing_cat = losing_cat + 1
            else: 
                reg_cat.append(losing_cat)
                losing_cat = 0

        result = [

            len(df["Position"]),
            self.helper.count_unique(df["Position"], 1),
            np.array(reg_tck).max(),
            round(float(self.helper.count_unique(df["Position"], 1)) / len(df["Position"]), 3),
            len(categorical["Position"]),
            self.helper.count_unique(categorical["Position"], 1),
            np.array(reg_cat).max(),
            round(float(self.helper.count_unique(categorical["Position"], 1)) / len(categorical["Position"]), 3),
            round(df["Distances"].mean() / df["CalcTime"].mean(), 3),
            round(categorical["Distances"].mean() / categorical["CalcTime"].mean(), 3),
            dates[0] / 12,
            dates[1]
        ]
        
        return result

    def get_dogs(self, page_html, type_dogs, a=False, b=False):
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
                if dog_place == 1 or dog_place == 2:
                    row.append(0)
                elif dog_place == 3 or dog_place == 4:
                    row.append(1)
                elif dog_place == 5 or dog_place == 6:
                    row.append(2)

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