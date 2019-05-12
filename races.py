# ----------------------------------------------------
# Races class
# ----------------------------------------------------

from datetime import datetime
import re
import click

class Races:

    def __init__(self, url, driver):

        self.url = url
        self.driver = driver

        self.result_page = self.driver.get(
            "https://greyhoundbet.racingpost.com/%s" % self.url,
            element_wait="dog-result-details",
            type_element="class")



    def dogs(self):
        # Variables
        self.dogs = list()
        for result in self.result_page.find_all("div", class_="container"):
            place = int(re.sub("\D", "", result.find("div", class_="place").text.replace(" ", "")))
            name  = result.find("div", class_="name").text[72:-32]
            link  = result.find("a", class_="details").attrs["href"]
            trap  = int(result.find("div", class_="holder").find("div").attrs["class"][1].replace("trap", ""))
            self.dogs.append([place, name, link, trap])
        return self.dogs

    def informations(self):
        self.informations = [
            self.result_page.find("span", class_="rTitle").text[:-9],
            datetime.strptime(self.result_page.find("span", class_="rTitle").text[-8:], "%d/%m/%y"),
            re.search("\((.*?)\)", self.result_page.find("span", {"id":"circle-race-title"}).text).group(0).replace("(", "").replace(")", ""),
            int(re.search("\)(.*?)m", self.result_page.find("span", {"id":"circle-race-title"}).text).group(0).replace(")", "").replace(" ", "").replace("m", ""))
        ]
        click.echo("--> Ready to access (%s, %s, %s, %s) " % (tuple(self.informations)))
        return self.informations
