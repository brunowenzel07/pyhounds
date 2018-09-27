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
from string import digits

def run(url):
    driver = webdriver.Chrome()
    tracks = Tracks(url, driver)
    dogs = Dogs()
    helper = Helper()
    db = Database("data/data_train.csv")
    with click.progressbar(tracks.get_tracks(), label="Training text") as bar:
        for track in bar:
            page_html = helper.get_page_code("http://greyhoundbet.racingpost.com/%s" % track, driver, type_wait="class", element_wait="meetingResultsList")
            for dog in dogs.get_dogs(page_html, "meetings"):
                dog_page = helper.get_page_code(
                    "http://greyhoundbet.racingpost.com/" + dog[2], 
                    driver, 
                    type_wait="id",
                    element_wait="sortableTable")
                for tr in dog_page.find("table", {"id":"sortableTable"}).find_all("tr", class_="row"):
                    what = tr.find_all("td")[9].text.encode("utf-8").replace("/", " ").replace("&", " ").replace(",", " ").replace("-", " ").translate(None, digits)
                    finished = tr.find_all("td")[6].text.encode("utf-8").replace("\xc2\xa0", "").replace("st", "").replace("nd", "").replace("rd", "").replace("th", "")
                    try:
                        if int(finished) < 3: result = 1
                        else : result = -1
                    except Exception:
                        if finished == "NR":
                            result = -1
                        else:
                            pass
                    finally:
                        if len(what) > 0:
                            row = [str(what), result]
                        with open("data/comments.csv", "a") as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow(row)

        driver.close()
