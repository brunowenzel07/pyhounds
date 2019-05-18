# ----------------------------------------------------
# Dogs class
# ----------------------------------------------------

# Libraries
import pandas as pd
from datetime import datetime
import numpy as np
import click

# Classes
import helper as hp

class Dogs:

    def __init__(self, dog, race, driver, t_=False):

        self.driver = driver
        self.dog    = dog
        self.race   = race

        if t_== "train":
            self.date = self.race["date"]
        elif t_ == "predict":
            self.date = datetime.today()

        self.result_page = self.driver.get(
            "https://greyhoundbet.racingpost.com/%s" % self.dog["link"],
            element_wait="formGrid",
            type_element="class")

        self.dataframe()

        click.echo(
            "--> Retreiving data: %s, %s, %s, %s" % (tuple(dog.values()))
        )


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
        self.df = self.df[self.df["date"]  < self.date]
        self.df = self.df.dropna(subset=["position"], axis=0)

    def stats(self):
        # Declare variables
        dog_features   = list()
        for r in [5,10,15]:
            s_ = self.df[:r]
            _tmp = np.array([
                # Frequency at distance
                float(len(s_[s_["distance"] == self.race["distance"]]))/r,
                # Frequency at trap
                float(len(s_[s_["trap"]     == self.dog["trap"]]))/r,
                # Frequency at grade
                float(len(s_[s_["grade"]    == self.race["grade"]]))/r,
                # Frequency at third positions
                float(len(s_[s_["position"] <= 3])) / r,
                # Frequency at last positions
                float(len(s_[s_["position"] > 3])) / r,
                np.mean(s_["bends"])
            ])
            dog_features.append(np.round(_tmp, 2))
        self.dog_stats = np.array(dog_features).reshape(1,18)[0]
        self.dog_stats = np.append(self.dog_stats, (self.date - self.df["date"].iloc[0]).days)
        # self.dog_stats = np.append(self.dog_stats, self.place)
        # self.dog_stats = np.append(self.dog_stats, self.dog["trap"])
        return self.dog_stats
