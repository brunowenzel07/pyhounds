from selenium import webdriver 
import click 
from database import Database
import sys 
sys.path.insert(0, "functions/")
from tracks import Tracks
from dogs import Dogs
from helper import Helper


def run(url):
    print("cu")
    driver = webdriver.Chrome()
    tracks = Tracks(url, driver)
    dogs = Dogs()
    helper = Helper()
    db = Database("data/data_train.csv")
    with click.progressbar(tracks.get_tracks()) as bar:
        for track in bar:
            page_html = helper.get_page_code("http://greyhoundbet.racingpost.com/%s" % track, driver, type_wait="class", element_wait="meetingResultsList")
            for dog in dogs.get_dogs(page_html, "meetings"):
                stat = dogs.get_stats(dog, driver)
                if int(dog[0]) <= 2: result = 0
                else: result = 1
                stat.append(result)
                db.insert(stat, "solo") 

    driver.close()