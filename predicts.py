#
# Process predict page
#

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re 
import pandas as pd 
from datetime import datetime 
import numpy as np 
from time import sleep
import click 
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
names = [
    "DA_TY_1", "DA_TY_2", "DA_TY_3", "DA_TY_4",    
    "DA_LY_1", "DA_LY_2", "DA_LY_3", "DA_LY_4",    
    "DA_T3_TMIN"  , "DA_T3_TMEAN",
    "DA_T3_BENDS" , "DA_T3_FIN",
    "DA_T12_TMIN" , "DA_T12_TMEAN",
    "DA_T12_BENDS", "DA_T12_FIN",
    "DB_TY_1", "DB_TY_2", "DB_TY_3", "DB_TY_4",    
    "DB_LY_1", "DB_LY_2", "DB_LY_3", "DB_LY_4",    
    "DB_T3_TMIN"  , "DB_T3_TMEAN",
    "DB_T3_BENDS" , "DB_T3_FIN",
    "DB_T12_TMIN" , "DB_T12_TMEAN",
    "DB_T12_BENDS", "DB_T12_FIN",
    "RES"
]

features = [
    "TY_1", "TY_4",    
    "LY_1", "LY_4",    
    "T3_TMIN"  , "T3_TMEAN",
    "T3_BENDS" , "T3_FIN",
    "T12_TMIN" , "T12_TMEAN",
    "T12_BENDS", "T12_FIN"
]

class Predicts:

    def __init__(self, driver, url, trap_a, trap_b):
        
        click.echo("--> Initialization script...")
        self.driver = driver 
        self.url = url 
        self.a = int(trap_a )
        self.b = int(trap_b)
        click.echo("--> Loading track page...")
        self.driver.get(url)
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "cardTabContainer")))
        self.results_page = BeautifulSoup(self.driver.page_source, "html.parser")

        click.echo("--> Loading classifier")
        self.clf = RandomForestClassifier(n_estimators=50, min_samples_leaf=100)
        df = pd.read_csv("data/dataset.csv", names=names)
        df.dropna(inplace=True)
        df.drop_duplicates(keep = False, inplace = True)
        self.X = pd.DataFrame(columns=features)
        click.echo("--> Train classifier")
        for x_col in features:
            self.X[x_col] = df[["DA_"+x_col, "DB_"+x_col]].apply(self.std, axis=1)
        self.clf.fit(self.X, df["RES"])

    def predict(self, X):
        return self.clf.predict_proba(X)

    def std(self, s):
        if s[0] == 0 or s[0] == s[1]:
            return 0.0
        else:
            return s[0] / (s[0] + s[1])

    def avg_bends(self, data):
        return np.average(np.array(data).astype(np.int))

    def normalize(self, bs_element, t_):
        if t_ == "sp":
            if len(bs_element) == 2:
                e_ = list()
                for b in bs_element:
                    e_.append(float(re.sub("\D", "", b)))
                return e_[0] / e_[1]
            else:
                return float("NaN")
        if t_ == "split":
            if len(bs_element) != 0:
                return float(bs_element)
            else:
                return float("NaN")
        if t_ == "gng":
            if len(bs_element) > 1:
                return float(bs_element)
            else:
                return 0

    def get_race_infos(self):
        return [
            re.search("- (.*?)m ", self.results_page.find("span", {"id":"title-circle-container"}).find("p", class_="p1").text).group(1),
            self.results_page.find("div", class_="pageHeader").find("h2").text,
            self.results_page.find("h3", {"id":"pagerCardTime"}).text
        ]

    def get_dogs(self):
        self.dogs = []
        for result in self.results_page.find_all("div", class_="runnerBlock"):
            name = result.find("a", class_="gh").find("strong").text[1:-1]
            link = result.find("a", class_="gh").attrs["href"]
            comment = result.find("p", class_="comment").text
            trap = int(result.find("a", class_="gh").find("i").attrs["class"][1].replace("trap", ""))
            if trap in [self.a, self.b]:
                self.dogs.append([name, link, comment, trap])        
        return self.dogs 

    def get_dog_stats(self, dog, race):
        df = pd.DataFrame()
        rows = list()
        stats = []
        url = "https://greyhoundbet.racingpost.com/" + dog[1]
        # Requesting race page 
        click.echo("--> Acessing url: " + url)
        self.driver.get(url)
        sleep(5)
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "runnerBlock")))
        html_page = BeautifulSoup(self.driver.page_source, "html.parser")        
        
        trs = html_page.find("table", {"id":"sortableTable"}).find("tbody").find_all("tr", class_="row")
        dog_comments = list()
        for tr in trs:
            c = tr.find_all("td")
            try:
                row = [
                    datetime.strptime(c[0].text.replace(" ", ""), "%d%b%y"),
                    c[2].text.replace("m", ""),
                    float(c[3].text.replace("[", "").replace("]", "")),
                    list(c[5].text.replace("-","")),
                    re.sub("\D", "", c[6].text),
                    c[9].text.encode("utf-8").decode("utf-8"),
                    c[10].text,            
                    c[14].text,
                    c[15].text,
                ]
                for s in c[9].text.split(","):        
                    for po in re.sub("[0-9]", "" ,s).split('&'):
                        if po != "":
                            dog_comments.append(po)
                rows.append(row)
            except Exception as a:
                pass


        df = pd.DataFrame(rows, columns=[
                    "date","dis","trp",
                    "bends","fin","rmks","wntm",
                    "grade","caltm"])
        df = df[df["date"] < datetime.now()]  
        df.replace('', np.nan, inplace=True)
        df.dropna(inplace=True)
        df["bends"] = df["bends"].apply(self.avg_bends)
        frequents = dog_comment.comment.value_counts()[:5]
        traps = df.trp.value_counts().index.values[:2]

        this_year = df[df["date"].dt.year == datetime.now().year]
        last_year = df[df["date"].dt.year == datetime.now().year - 1]
      
        if len(this_year) > 1 and len(last_year) > 1:

            s = [
                len(this_year[this_year["fin"].astype(np.float) == 1]) / len(this_year),
                len(this_year[this_year["fin"].astype(np.float) == 4]) / len(this_year),
                len(last_year[last_year["fin"].astype(np.float) == 1]) / len(last_year),
                len(last_year[last_year["fin"].astype(np.float) == 4]) / len(last_year),
                this_year[this_year["dis"].astype(np.float) == float(race[0])]["caltm"][:3].astype(np.float).min(),
                this_year[this_year["dis"].astype(np.float) == float(race[0])]["caltm"][:3].astype(float).mean(),
                df.iloc[:3]["bends"].astype(np.float).mean(),
                df.iloc[:3]["fin"].astype(np.float).mean(),    
                this_year[this_year["dis"].astype(np.float) == float(race[0])]["caltm"][:12].astype(np.float).min(),
                this_year[this_year["dis"].astype(np.float) == float(race[0])]["caltm"][:12].astype(float).mean(),
                df.iloc[:12]["bends"].astype(np.float).mean(),
                df.iloc[:12]["fin"].astype(np.float).mean(),
            ]

            stats = list(np.round(s, 3))
            return stats, frequents, traps

        else:
            return [], [], []