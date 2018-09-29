from selenium import webdriver 
import click 
from database import Database
import sys 
sys.path.insert(0, "functions/")
from tracks import Tracks
from dogs import Dogs
from helper import Helper


chrome_options = webdriver.ChromeOptions()
prefs={
    "profile.managed_default_content_settings.images": 2, 
    "profile.managed_default_content_settings.stylesheet": 2, 
    'disk-cache-size': 8192 
    }
chrome_options.add_experimental_option('prefs', prefs)

def run(url):   
    print(chrome_options)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    tracks = Tracks(url, driver, "results")
    dogs = Dogs()
    helper = Helper()
    db = Database("data/data_train.csv")
    with click.progressbar(tracks.get_tracks()) as bar:
        for track in bar:
            page_html = helper.get_page_code("http://greyhoundbet.racingpost.com/%s" % track, driver, type_wait="class", element_wait="meetingResultsList")
            for dog in dogs.get_dogs(page_html, "meetings"):
                stat = dogs.get_stats(dog, driver)
                if len(stat) > 0:
                    if int(dog[0]) <= 2: result = 0
                    else: result = 1
                    stat.append(result)
                    db.insert(stat, "solo") 
    driver.close()

