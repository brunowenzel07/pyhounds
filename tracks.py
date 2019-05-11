# -*- coding: UTF-8
# !/usr/bin/python
from helper import Helper
from bs4 import BeautifulSoup
import re

class Tracks:

    def __init__(self, date=False, url=False, driver=False, type_track=False):

        if date:
            self.url = "http://greyhoundbet.racingpost.com/#results-list/r_date=%s" % date
        else:
            self.url = url

        self.driver = driver
        self.type = type_track
        self.helper = Helper()

    def get_track_stats(self, page_html):
        title = page_html.find("div", class_="pageHeader").find("h2").text.encode("utf-8")
        time = page_html.find("h3", {"id":"pagerCardTime"}).text.encode("utf-8")
        return [title,time]

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
            pass
        return tracks
