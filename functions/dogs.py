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
    
    def get_stats(self, dog, driver):
        
        dog_page = self.helper.get_page_code(
            "http://greyhoundbet.racingpost.com/" + dog[2], 
            driver, 
            type_wait="id",
            element_wait="sortableTable")

        positions = []
        weight = []
        ratio_time = []
        ratio_split = []
        total = []
        result = []

        if dog[0] < 3: dog_result = 0
        else: dog_result = 1
        try: 
            for tr_content in dog_page.find("table", {"id":"sortableTable"}).find_all("tr", class_="row")[:15]:
                race_data = Race(tr_content.find_all("td")).race()
                if len(race_data) == 8:               
                    positions.append(race_data[2])
                    weight.append(race_data[6])
                    result.append(race_data[-1])
                    ratio_time.append(round((race_data[4] - race_data[5])/race_data[5], 4))
                    ratio_split.append(round((race_data[1] - (race_data[5]/5)) / (race_data[5]/5),4))            
                    total.append(race_data)

            whelping = self.helper.normalize(dog_page.find("table", class_="pedigree").find_all("td")[3], "whelping")

            frame = {
                "PositionsDiff" : positions,
                "Weight" : weight,
                "RatioTime" : ratio_time,
                "RatioSplit" : ratio_split,
                "Result" : result
            }

            df = pd.DataFrame(data=frame)

            unique, counts = np.unique(result, return_counts=True)

            
            if len(unique) == 2:
                stats_avg = [
                    round(df["PositionsDiff"].mean(), 3),
                    round(df["Weight"].mean(), 3),
                    round(df["RatioTime"].mean(), 3),
                    round(df["RatioSplit"].mean(), 3),
                    round(float(counts[0])/sum(counts), 4),
                    round(float(counts[1])/sum(counts), 4),
                    whelping,
                    dog_result
                ]     
            else:
                stats_avg = []

            return stats_avg

        except Exception as a:
            print(a)
            return []

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
        return rows
