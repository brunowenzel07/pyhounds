# ----------------------------------------------------
# Races class
# ----------------------------------------------------

from datetime import datetime
import re
import click
import helper as hp 

class Races:

    def __init__(self, infos=False, driver=False, t_=False, link=False):
        self.infos        = infos 
        self.driver       = driver        
        self.dogs         = list()

        if t_== "train":
            self.url = "https://greyhoundbet.racingpost.com/" + link
            self.type_element = "class"
            self.element_wait = "dog-result-details"
            
        elif t_ == "predict":
            self.url = self.infos["link"]
            self.type_element = "id"
            self.element_wait = "cardTab-card"

        click.echo("--> Loading the url: %s" % self.url )
        
        self.card_page = self.driver.get(
            self.url,
            element_wait=self.element_wait,
            type_element=self.type_element
        )

    def train_dogs(self):
        # Variables
        # "https://greyhoundbet.racingpost.com/%s" %
        self.dogs = list()
        for result in self.card_page.find_all("div", class_="container"):
            place = int(re.sub("\D", "", result.find("div", class_="place").text.replace(" ", "")))
            name  = result.find("div", class_="name").text[72:-32]
            link  = result.find("a", class_="details").attrs["href"]
            trap  = int(result.find("div", class_="holder").find("div").attrs["class"][1].replace("trap", ""))
            self.dogs.append({
                "place" : place,
                "dog"   : name,
                "link"  : link,
                "trap"  : trap
            })
        return self.dogs

    def train_informations(self):
        self.informations = {
            "track"    : self.card_page.find("span", class_="rTitle").text[:-9],
            "date"     : datetime.strptime(self.card_page.find("span", class_="rTitle").text[-8:], "%d/%m/%y"),
            "grade"    : re.search("\((.*?)\)", self.card_page.find("span", {"id":"circle-race-title"}).text).group(0).replace("(", "").replace(")", ""),
            "distance" : int(re.search("\)(.*?)m", self.card_page.find("span", {"id":"circle-race-title"}).text).group(0).replace(")", "").replace(" ", "").replace("m", ""))
        }
        click.echo("--> Ready to access (%s, %s, %s, %s) " % (tuple(self.informations)))
        return self.informations

    def future_dogs(self):
        for block in self.card_page.find_all("div", class_="runnerBlock"):
            runner_block = {
                "link"    : block.find("a").attrs["href"],
                "trap"    : int(block.find("i").attrs["class"][1].replace("trap", "")),
                "name"    : block.find("strong").text[1:],
                "comment" : block.find("p", class_="comment").text,
                "date"    : datetime.now(),
            }
            self.dogs.append(runner_block)
        return self.dogs

    def future_informations(self):
        s = self.card_page.find("span", {"id":"title-circle-container"}).find("span", class_="titleColumn2").text        
        
        return {
            "name"       : self.card_page.find("div", class_="pageHeader").find("h2").text,
            "time_label" : self.infos["time_label"],
            "grade"      : re.search("(.*?) - ", s).group(1),
            "distance"   : int(re.search("- (.*?)m", s).group(1)),
            "time"       : self.infos["date"] + " " + self.infos["time_label"],
        }
