from selenium import webdriver 
import click 
from database import Database
import sys 
sys.path.insert(0, "functions/")
from tracks import Tracks
from dogs import Dogs
from helper import Helper
from datetime import datetime 


chrome_options = webdriver.ChromeOptions()
prefs={
    "profile.managed_default_content_settings.images": 2, 
    "profile.managed_default_content_settings.stylesheet": 2, 
    'disk-cache-size': 8192 
    }
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_argument("--headless")

def run(url):   
    # Create a instance for webdriver 
    driver = webdriver.Chrome(chrome_options=chrome_options)
    
    # Get tracks for URL 
    tracks = Tracks(url, driver, "results")

    # Instance of dogs
    dogs, helper = Dogs(), Helper()

    # Create a instance for remarks classifier    
    remarks_clf = helper.remarks_clf()

    # Load data train file 
    db = Database("data/data_train.csv")

    with click.progressbar(tracks.get_tracks()) as bar1:
        for track in bar1:
            # Get page of track 
            page_html = helper.get_page_code("http://greyhoundbet.racingpost.com/%s" % track, driver, type_wait="class", element_wait="meetingResultsList")

            with click.progressbar(dogs.get_dogs(page_html, "meetings")) as bar2:
                # Iterate about dogs in page
                for dog in bar2:

                    # Receive dog_page 
                    dog_page = dogs.get_page(dog,driver)
                    
                    # Auxiliary array 
                    i = 0
                    dog_races = []

                    # Stats of dog 
                    stat = dogs.get_stats(dog, dog_page, remarks_clf)

                    if len(stat.values()) > 0:
                        s = stat.values()
                        s.append(dog[0])
                        
                        db.insert(s, "solo")     

                    
         
    driver.close()

