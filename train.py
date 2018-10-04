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
                i = 0
                dog_races = []
                thread1 = threading.Thread(target=dogs.get_stats, args=[dog, dog_page, remarks_clf, q, "train"])
                thread1.start()
                break 
        thread1.join()
        while not q.empty():
            stat = q.get()
            if len(stat) > 0:
                db.insert(stat, "solo")     
        break 
    driver.close()

