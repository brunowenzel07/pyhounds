from selenium import webdriver 
import click 
from database import Database
import sys 
sys.path.insert(0, "functions/")
from tracks import Tracks
from dogs import Dogs
from helper import Helper
from datetime import datetime 
import threading
import Queue
import time 
import multiprocessing
import re 

chrome_options = webdriver.ChromeOptions()
prefs={
    "profile.managed_default_content_settings.images": 2, 
    "profile.managed_default_content_settings.stylesheet": 2, 
    'disk-cache-size': 8192 
    }
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_argument("--headless")

def run(url):   
    print(url)
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

    url_date = re.search("(?:r_date=).*", url)
    url_date = datetime.strptime(url_date.group()[7:], "%Y-%m-%d")

    for track in tracks.get_tracks():
        # Get page of track 
        page_html = helper.get_page_code("http://greyhoundbet.racingpost.com/%s" % track, driver, type_wait="class", element_wait="meetingResultsList")        

        with click.progressbar(dogs.get_dogs(page_html, "meetings")) as bar2:
            # create a queue
            q = Queue.Queue()
            # Iterate about dogs in page
            for dog in bar2:
                # Receive dog_page 
                dog_page = dogs.get_page(dog,driver)

                # Auxiliary array 
                whelping, last_run = helper.get_dog_dates(dog_page, "train", url_date)
                print(whelping, last_run)
                dog_races = []
                thread1 = threading.Thread(target=dogs.get_stats, args=[dog, dog_page, remarks_clf, q, "train", url_date, whelping, last_run])
                thread1.start()
                
        thread1.join()
        while not q.empty():
            stat = q.get()
            if len(stat) > 0:
                db.insert(stat, "solo")     
    driver.close()

