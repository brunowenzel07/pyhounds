# -*- coding: UTF-8
# !/usr/bin/python 
from helper import Helper

class Tracks:
    
    def __init__(self, url, driver):

        self.url = url 
        self.driver = driver 
        
        if "results" in url:    
            self.type = "results"
        if "meeting" in url: 
            self.type = "meeting"


    def get_tracks(self):
        """ 
            Return all links for the tracks in url passed
        """
        helper = Helper()
        if self.type == "results":
            page_html = helper.get_page_code(self.url, self.driver, element_wait="results-race-name", type_wait="class")
            tracks = []
            for race_li in page_html.find("div", class_="meetings").find_all("li"):
                for race_link in race_li.find("div", class_="results-race-list-row").find_all("a"):
                    tracks.append(race_link.attrs["href"])
            return tracks