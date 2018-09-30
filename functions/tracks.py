# -*- coding: UTF-8
# !/usr/bin/python 
from helper import Helper
from bs4 import BeautifulSoup

class Tracks:
    
    def __init__(self, url, driver, type_track):

        self.url = url 
        self.driver = driver         
        self.type = type_track
        self.helper = Helper()
    def get_tracks(self):
        """ 
            Return all links for the tracks in url passed
        """
        
        if self.type == "results":
            page_html = self.helper.get_page_code(self.url, self.driver, element_wait="results-race-name", type_wait="class")
            tracks = []
            for race_li in page_html.find("div", class_="meetings").find_all("li"):
                for race_link in race_li.find("div", class_="results-race-list-row").find_all("a"):
                    tracks.append(race_link.attrs["href"])
        if self.type == "predicts":
            with open("html_files/to_pred.html", "r") as html_file:
                page_html = BeautifulSoup(html_file, "html.parser")
            tracks = []
            for race_li in page_html.find("ul", class_="raceListTime").find_all("li"):
                time = self.helper.normalize(race_li.find("strong"), "string")
                location = self.helper.normalize(race_li.find("h4"), "string")
                race = self.helper.normalize(race_li.find("h5"), "string")
                link = self.helper.normalize(race_li.find("a"), "link").replace("tab=form", "tab=card")
                track = [
                    time, location, race, link
                ]
                tracks.append(track)
        return tracks