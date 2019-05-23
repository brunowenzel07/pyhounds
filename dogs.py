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
            s = "%s-%s-%s" % (datetime.today().day, datetime.today().month, datetime.today().year)
            self.date = datetime.strptime(s, "%d-%m-%Y")

        self.result_page = self.driver.get(
            "https://greyhoundbet.racingpost.com/%s" % self.dog["link"],
            element_wait="formGrid",
            type_element="class")

        self.dataframe()

        click.echo(
            "--> Retreiving data: %s" % (self.dog["link"])
        )

        self.whelping = datetime.strptime(self.result_page.find("table", class_="pedigree").find_all("td")[-1].text.replace(" ", ""), "%d%b%y")

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
                hp.normalize(c[7],  "by"),
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
            "by",
            "remarks",
            "win_time",
            "weight",
            "grade",
            "cal_time"
        ])
        self.df = self.df[self.df["date"]  < self.date]
        self.df["split"] = self.df["split"].fillna(self.df["split"].mean())
        self.df["bends"] = self.df["bends"].fillna(self.df["bends"].mean())
        self.df = self.df.dropna(subset=["position"], axis=0)
        self.total_df = len(self.df)

    def extra_infos(self):
        gh_stats = list()
        for gh in self.result_page.find("ul", class_="ghStats").find_all("li"):
            s = np.array(gh.find("strong").text.split("/")).astype(float)
            gh_stats.append(s[0]/s[1])     
        return np.round(np.nan_to_num(gh_stats), 2)   

    def stats(self):
        # Total of wons at track, self.race["distance"], self.dog["trap"] and self.race["grade"]
        stats = {
            "full"       : len(self.df[(self.df["local"]    == self.race["track"]) & (self.df["distance"] == self.race["distance"]) & (self.df["grade"] == self.race["grade"]) & (self.df["trap"] == self.dog["trap"])]),
            "trap"       : len(self.df[(self.df["trap"]     == self.dog["trap"])]),
            "distance"   : len(self.df[(self.df["distance"] == self.race["distance"])]),
            "local"      : len(self.df[(self.df["local"]    == self.race["track"])]),
            "grade"      : len(self.df[(self.df["grade"]    == self.race["grade"])]),
            "dist_trap"  : len(self.df[(self.df["distance"] == self.race["distance"]) & (self.df["trap"] == self.dog["trap"])]),
            "dist_grade" : len(self.df[(self.df["distance"] == self.race["distance"]) & (self.df["grade"] == self.race["grade"])]),
            "first_full" : len(self.df[(self.df["local"]    == self.race["track"]) & (self.df["distance"] == self.race["distance"]) & (self.df["grade"] == self.race["grade"]) & (self.df["trap"] == self.dog["trap"]) & (self.df["position"] <= 2)]),
            "first_trap" : len(self.df[(self.df["trap"]     == self.dog["trap"]) & (self.df["position"] <= 2)]),
            "first_dist" : len(self.df[(self.df["distance"] == self.race["distance"]) & (self.df["position"] <= 2)]),
            "first_local": len(self.df[(self.df["local"]    == self.race["track"]) & (self.df["position"] <= 2)]),
            "first_grade": len(self.df[(self.df["grade"]    == self.race["grade"]) & (self.df["position"] <= 2)]),
            "tree_full"  : len(self.df[(self.df["local"]    == self.race["track"]) & (self.df["distance"] == self.race["distance"]) & (self.df["grade"] == self.race["grade"]) & (self.df["trap"] == self.dog["trap"]) & (self.df["position"] >= 3)]),
            "tree_trap"  : len(self.df[(self.df["trap"]     == self.dog["trap"]) & (self.df["position"] >= 3)]),
            "tree_dist"  : len(self.df[(self.df["distance"] == self.race["distance"]) & (self.df["position"] >= 3)]),
            "tree_local" : len(self.df[(self.df["local"]    == self.race["track"]) & (self.df["position"] >= 3)]),
            "tree_grade" : len(self.df[(self.df["grade"]    == self.race["grade"]) & (self.df["position"] >= 3)]),  
            "mean_time"   : self.df[(self.df["position"] != 1) & (self.df["distance"] == self.race["distance"]) & (self.df["grade"] ==self.race["grade"]) & (self.df["local"] ==self.race["track"])]["cal_time"].mean(),
            "min_time"    : self.df[(self.df["position"] != 1) & (self.df["distance"] == self.race["distance"]) & (self.df["grade"] ==self.race["grade"]) & (self.df["local"] ==self.race["track"])]["cal_time"].min(),
            "max_time"    : self.df[(self.df["position"] != 1) & (self.df["distance"] == self.race["distance"]) & (self.df["grade"] ==self.race["grade"]) & (self.df["local"] ==self.race["track"])]["cal_time"].max(),
            "by_mean_lost": self.df[(self.df["position"] != 1) & (self.df["distance"] == self.race["distance"]) & (self.df["grade"] ==self.race["grade"]) & (self.df["local"] ==self.race["track"])]["by"].mean(),
            "by_mean_win" : self.df[(self.df["position"] == 1) & (self.df["distance"] == self.race["distance"]) & (self.df["grade"] ==self.race["grade"]) & (self.df["local"] ==self.race["track"])]["by"].mean(),
            "bends_mean"  : self.df[(self.df["distance"] == self.race["distance"]) & (self.df["grade"] ==self.race["grade"]) & (self.df["local"] ==self.race["track"])]["bends"].mean(),
            "position"    : self.df[(self.df["distance"] == self.race["distance"]) & (self.df["grade"] ==self.race["grade"]) & (self.df["local"] ==self.race["track"])]["position"].mean(),
            "days_lr"     : float((self.date - self.df["date"].iloc[0]).days),
            "whelping"    : (self.date - self.whelping).days,
        }
        self.stats = stats
        return self.stats

