# -*- coding: UTF-8
# !/usr/bin/python 
from helper import Helper
from races import Race
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

    def get_stats(self, dog, dog_page, remarks_clf, stat_type, q, url_date, whelping, last_run):

        # Define dog trap 
        dog_trap = dog[3]
        
        i, dog_races = 0, []
        for tr_content in dog_page.find("table", {"id":"sortableTable"}).find_all("tr", class_="row"):            
            try: 
                tds = tr_content.find_all("td")
                run_date_tr = datetime.strptime(tds[0].text.encode("utf-8").replace(" ", ""),"%d%b%y")                
                if run_date_tr < url_date:
                    dog_age = self.helper.normalize(dog_page.find("table",class_="pedigree").find_all("td")[3], "date")
                    race = Race(tds, dog[3])
                    race_data = race.calculate_stats(race.normalize_stats(), remarks_clf)
                    dog_races.append(race_data)
                    i += 1 
            except Exception as a :
                pass                 
        
        try:

            df = pd.DataFrame(data=dog_races, columns=["bends", "remarks", "finishes", "gng","sp","trap","weight","split"])
            print(dog)
            result = [                
                # Média da troca de posições nas últimas 5 corridas
                df["bends"].mean(),
                # Comentários positivos para os últimas corridas
                self.helper.count_unique(df["remarks"].tolist(), 0),
                # Top 1
                self.helper.count_unique(df["finishes"].tolist(), 1),
                # Top 2
                self.helper.count_unique(df["finishes"].tolist(), 1) + self.helper.count_unique(df["finishes"].tolist(), 2),
                # Top 3
                self.helper.count_unique(df["finishes"].tolist(), 1) + self.helper.count_unique(df["finishes"].tolist(), 2) + self.helper.count_unique(df["finishes"].tolist(), 3),
                # gng avg
                round(df["gng"].mean(), 3),
                # Weight
                round(df["weight"][0], 3),
                # split
                round(df["split"].mean(), 3),
                whelping,
                last_run,                
            ]

            if stat_type == "train": result.append(int(dog[0]))
            else: result.append(int(dog[-1]))
            
        except Exception as a:
            result = []
        q.put(result)

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
