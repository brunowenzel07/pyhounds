import pandas as pd
from tracks import Tracks
from races import Races
from dogs import Dogs
from bs4 import BeautifulSoup
from helper import Helper

from datetime import datetime

def main(dog):
    helper = Helper()
    dogs = Dogs()
    dog_page = BeautifulSoup(open("tmp/dog%s.html" % dog, "r"), "html.parser")
    dates = helper.get_dog_dates(dog_page, datetime.strptime("2018-10-17", "%Y-%m-%d"))
    dog = [1, "Droppys Act", "#results-dog/race_id=1646685&dog_id=518586&r_date=2018-10-17&track_id=39&r_time=11:03", 1]
    track = ["462", "A2"]
    dog_stats = dogs.get_stats(dog, dog_page, dates, track)

if __name__ == "__main__":
    for i in [1,2]:
        main(i)