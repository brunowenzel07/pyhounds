import pandas as pd
from tracks import Tracks
from races import Races
from dogs import Dogs
from bs4 import BeautifulSoup
from helper import Helper
from database import Database
from datetime import datetime

# Create instance of classes
helper, dogs, tracks = Helper(), Dogs(), Tracks()

db = Database("data/data_train.csv")

# Get track informations
page_html = BeautifulSoup(open("tmp/dog.html", "r"), "html.parser")      
track_stats = tracks.get_track_stats(page_html)

stats = []
for dog in dogs.get_dogs(page_html,"predicts", a="1", b="2"):
    try:
        if int(dog[0]) != 3 and int(dog[0]) != 4:
            dog_page = dogs.get_page(dog,driver)
            dates = helper.get_dog_dates(dog_page, datetime.strptime(date, "%Y-%m-%d"))
            dog_stats = dogs.get_stats(dog, dog_page, dates, track_stats)                    
            if len(dog_stats) > 0:
                stats.append(dog_stats)
    except Exception as a:
        print(a)

print(stats)