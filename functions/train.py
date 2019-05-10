# !/usr/bin/python 
import sys 
from selenium import webdriver 
import click 
from datetime import datetime 

sys.path.insert(0, "classes/")
from tracks import Tracks
from helper import Helper
from dogs import Dogs 
from database import Database

# Define options for the headless browser 
chrome_options = webdriver.ChromeOptions()
prefs={
    "profile.managed_default_content_settings.images": 2, 
    "profile.managed_default_content_settings.stylesheet": 2, 
    'disk-cache-size': 8192 
    }
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_argument("--headless")

def run(date):

    # Create a instance for webdriver 
    driver = webdriver.Chrome(chrome_options=chrome_options)

    # Get track for date 
    tracks = Tracks(date=date, driver=driver, type_track="results")

    # Create instance of classes
    helper, dogs = Helper(), Dogs()

    db = Database("data/data_train.csv")

    for track in tracks.get_tracks():

        click.echo("Getting data from: %s" % track)

        page_html = helper.get_page_code("http://greyhoundbet.racingpost.com/%s" % track, driver, type_wait="class", element_wait="meetingResultsList")        
        track_stats = tracks.get_track_stats(page_html)

        click.echo("Creating a queue with dogs data")

        stats = []
        for dog in dogs.get_dogs(page_html, "meetings"):            
            try:
                if int(dog[0]) != 3 and int(dog[0]) != 4:
                    dog_page = dogs.get_page(dog,driver)
                    dates = helper.get_dog_dates(dog_page, datetime.strptime(date, "%Y-%m-%d"))
                    dog_stats = dogs.get_stats(dog, dog_page, dates)                    
                    if len(dog_stats) > 0:
                        dog_stats.append(int(dog[0]))
                        stats.append(dog_stats)
            except Exception as a:
                print(a)
        
        for i, s in enumerate(stats):
            for k, t in enumerate(stats):
                try: 
                    row = s[:-1] + t[:-1]
                    a_position = int(s[-1])
                    b_position = int(t[-1])
                    if a_position != b_position:
                        if a_position == 1 and b_position == 6:                            
                            print(row.append(0))
                            db.insert(row, "solo")
                        elif a_position == 5 and b_position == 2: 
                            print(row.append(1))
                            db.insert(row, "solo")                        
                except Exception as a:
                    pass
