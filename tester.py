from selenium import webdriver 
import click 
from database import Database
import csv 
import sys 
sys.path.insert(0, "functions/")
from tracks import Tracks
from dogs import Dogs
import numpy as np 
from helper import Helper
from selenium.webdriver.common.proxy import Proxy, ProxyType

def run(url):
    driver = webdriver.Chrome()
    tracks = Tracks(url, driver)
    dogs = Dogs()
    helper = Helper()
#    db = Database("data/txt_comments.csv")
    for track in tracks.get_tracks():
        page_html = helper.get_page_code("http://greyhoundbet.racingpost.com/%s" % track, driver, type_wait="class", element_wait="meetingResultsList")
        comments = []
        for tr in page_html.find("table", {"id":"sortableTable"}).find("tbody").find_all("tr")[1:]: 
            print(tr)
#            for i in tr.find_all("td")[9].text.encode("utf-8").split(","):
#                comments.append(i)
#        a, b = np.unique(comments, return_counts=True)   
#        
#        with open("data/txt_comments.csv", "a") as csvfile:
#            writer = csv.writer(csvfile)      
#            writer.writerow(a)

    driver.close()




def run(url):
    driver = webdriver.Chrome()
    tracks = Tracks(url, driver)
    dogs = Dogs()
    helper = Helper()
    db = Database("data/data_train.csv")
    for track in tracks.get_tracks():
        page_html = helper.get_page_code("http://greyhoundbet.racingpost.com/%s" % track, driver, type_wait="class", element_wait="meetingResultsList")
        for dog in dogs.get_dogs(page_html, "meetings"):
            dog_page = helper.get_page_code(
                "http://greyhoundbet.racingpost.com/" + dog[2], 
                driver, 
                type_wait="id",
                element_wait="sortableTable")
            dog_comments = []
            for tr in dog_page.find("table", {"id":"sortableTable"}).find_all("tr", class_="row"):
                what = tr.find_all("td")[9].text.encode("utf-8").split(",")
                with open("data/txt_comments.csv", "a") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(what)
    driver.close()