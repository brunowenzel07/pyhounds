# -*- coding: UTF-8
# !/usr/bin/python 
from selenium import webdriver 
import bot 
import click 
from database import Database

def run(url):
    driver = webdriver.Chrome()
    db = Database("races.csv")
    with click.progressbar(bot.get_results_tracks(url, driver)) as bar:
        for track in bar:
            stats = bot.get_races_results(track, driver)
            db.insert(stats)
    driver.close()