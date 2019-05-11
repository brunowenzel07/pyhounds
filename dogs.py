# ----------------------------------------------------
# Dogs class
# ----------------------------------------------------

# Libraries
import pandas as pd
from datetime import datetime

# Classes
import helper as hp

class Dogs:

    def __init__(self, dog, race, driver):

        self.driver                                     = driver
        self.place, self.dog, self.url, self.trap       = dog
        self.race, self.date, self.grade, self.distance = race

        self.result_page = self.driver.get(
            "https://greyhoundbet.racingpost.com/%s" % self.url,
            element_wait="formGrid",
            type_element="class")

        self.dataframe()

    def dataframe(self):
        stats = list()
        for tr in self.result_page.find("table", {"id":"sortableTable"}).find("tbody").find_all("tr", class_="row"):
            c = tr.find_all("td")
            stats.append([
                hp.normalize(c[0],  "date"),
                hp.normalize(c[1],  "text"),
                hp.normalize(c[2],  "distance"),
                hp.normalize(c[3],  "only_digits"),
                hp.normalize(c[4],  "float"),
                hp.normalize(c[5],  "bends"),
                hp.normalize(c[6],  "only_digits"),
                hp.normalize(c[9],  "remarks"),
                hp.normalize(c[10], "float"),
                hp.normalize(c[12], "float"),
                hp.normalize(c[14], "text"),
                hp.normalize(c[15], "float"),
            ])
        self.df = pd.DataFrame(stats, columns=[
            "date",
            "local",
            "distance",
            "trap",
            "split",
            "bends",
            "position",
            "remarks",
            "win_time",
            "weight",
            "grade",
            "cal_time"
        ])

    def stats(self):
        print(self.race)
        # Only races before this race
        self.df       = self.df[self.df["date"] < self.date]
        # Only cat races
        self.df_grade = self.df[self.df["grade"] = self.grade]
        # Only distace
        self.df_dist  = self.df[self.df["dist"]  = self.dist]
