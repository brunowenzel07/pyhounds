# -*- coding: UTF-8
# !/usr/bin/python
from bs4 import BeautifulSoup
import sys 
sys.path.insert(0, "functions/")
from dogs import Dogs
from races import Race

dogs = Dogs()

with open("html_files/race.html", "r") as html_page:
    page_html = BeautifulSoup(html_page, "html.parser")

for tr_content in page_html.find("table", {"id":"sortableTable"}).find_all("tr", class_="row"):
    race = Race(tr_content.find_all("td"))
    calculated_data = race.calculate_stats(race.normalize_stats())          
    break