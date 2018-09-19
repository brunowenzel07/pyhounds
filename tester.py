# -*- coding: UTF-8
# !/usr/bin/python 
from selenium import webdriver 
import bot 


def run(url):
    driver = webdriver.Chrome()
    for track in bot.get_results_tracks(url, driver):
        stats = bot.get_races_results(track, driver)
        break 
    driver.close()