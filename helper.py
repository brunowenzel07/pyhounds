# !/usr/bin/python 
from bs4 import BeautifulSoup
from requests import post 

class Helper():

    def __init__(self):
        pass

    def diary_dogs(self, driver):

        url = "http://greyhoundstats.co.uk/graded_greyhound_stats.php"        

        driver.get(url)
       
       