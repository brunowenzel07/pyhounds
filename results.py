#
# Process results pages
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

class Results:

    # init function
    def __init__(self, date, driver):

        self.date = date 
        self.driver = driver 
        # Load page of results 
        self.driver.get("https://greyhoundbet.racingpost.com/#results-list/r_date=%s" % self.date)
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "meetings")))
        self.results_page = BeautifulSoup(self.driver.page_source, "html.parser")

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

    def diff_time(self, data):
        return abs(float(data["wntm"]) - float(data["caltm"]))

    # Get dog stats
    def get_dog_stats(self, dog, race):
        df = pd.DataFrame()
        rows = list()
        stats = []

        # Requesting race page 
        click.echo("--> Acessing url: " + dog[-2])
        self.driver.get("https://greyhoundbet.racingpost.com/" + dog[-2])
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "sortableTable")))
        sleep(1)
        html_page = BeautifulSoup(self.driver.page_source, "html.parser")
        born = datetime.strptime(html_page.find("table", class_="pedigree").find_all("td")[-1].text.replace(" ", ""), "%d%b%y")
        trs = html_page.find(
            "div", class_="results-dog-details").find(
            "table", class_="formGrid").find(
            "tbody").find_all(
            "tr", class_="row")

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

        this_year = df[df["date"].dt.year == datetime.now().year]
        last_year = df[df["date"].dt.year == datetime.now().year - 1]
      
        if len(this_year) > 1 and len(last_year) > 1:

            s = [
                len(this_year[this_year["fin"].astype(np.float) == 1]) / len(this_year),
                len(this_year[this_year["fin"].astype(np.float) == 2]) / len(this_year),
                len(this_year[this_year["fin"].astype(np.float) == 3]) / len(this_year),
                len(this_year[this_year["fin"].astype(np.float) == 4]) / len(this_year),
                len(last_year[last_year["fin"].astype(np.float) == 1]) / len(last_year),
                len(last_year[last_year["fin"].astype(np.float) == 2]) / len(last_year),
                len(last_year[last_year["fin"].astype(np.float) == 3]) / len(last_year),
                len(last_year[last_year["fin"].astype(np.float) == 4]) / len(last_year),
                this_year[this_year["dis"].astype(np.float) == float(race[-1])]["caltm"][:3].astype(np.float).min(),
                this_year[this_year["dis"].astype(np.float) == float(race[-1])]["caltm"][:3].astype(float).mean(),
                df.iloc[:3]["bends"].astype(np.float).mean(),
                df.iloc[:3]["fin"].astype(np.float).mean(),    
                this_year[this_year["dis"].astype(np.float) == float(race[-1])]["caltm"][:12].astype(np.float).min(),
                this_year[this_year["dis"].astype(np.float) == float(race[-1])]["caltm"][:12].astype(float).mean(),
                df.iloc[:12]["bends"].astype(np.float).mean(),
                df.iloc[:12]["fin"].astype(np.float).mean(),
            ]

            stats = list(np.round(s, 3))
            return dog[:2] + [dog[-1]] + stats

        else:
            return []

    # Get informations about race 
    def get_race_infos(self, race):
        # Requesting race page 
        self.driver.get("https://greyhoundbet.racingpost.com/" + race)
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "meetingResultsList")))
        html_page = BeautifulSoup(self.driver.page_source, "html.parser")

        return [
            html_page.find("span", class_="rTitle").text[:-9],
            datetime.strptime(html_page.find("span", class_="rTitle").text[-8:], "%d/%m/%y"),
            re.search("\((.*?)\)", html_page.find("span", {"id":"circle-race-title"}).text).group(0).replace("(", "").replace(")", ""),
            re.search("\)(.*?)m", html_page.find("span", {"id":"circle-race-title"}).text).group(0).replace(")", "").replace(" ", "").replace("m", "")
        ]

    # get links on results page
    def get_links(self):
        # Getting links
        self.results_links = list()
        for headline in self.results_page.find_all("div", class_="results-race-list-row"):
            for link in headline.find_all("a"):
                self.results_links.append(link.attrs["href"])    
        return self.results_links

    # get dogs of race
    def get_dogs(self, race):
        # Variables
        dogs = list()        
        # Requesting race page 
        self.driver.get("https://greyhoundbet.racingpost.com/" + race)
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "meetingResultsList")))
        html_page = BeautifulSoup(self.driver.page_source, "html.parser")

        for result in html_page.find_all("div", class_="container"):
            place = int(re.sub("\D", "", result.find("div", class_="place").text.replace(" ", "")))
            name = result.find("div", class_="name").text[72:-32]
            link = result.find("a", class_="details").attrs["href"]
            trap = int(result.find("div", class_="holder").find("div").attrs["class"][1].replace("trap", ""))
            dogs.append([place, name, link, trap])
        return dogs
