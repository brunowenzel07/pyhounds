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

def run(trap_a, trat_b):

    # Create a instance for webdriver 
    driver = webdriver.Chrome(chrome_options=chrome_options)

    # Create instance of classes
    helper, dogs, tracks = Helper(), Dogs(), track()

    db = Database("data/data_train.csv")
