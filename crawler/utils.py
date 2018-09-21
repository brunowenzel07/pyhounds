# -*- coding: UTF-8
# !/usr/bin/python 
from requests import get
from bs4 import BeautifulSoup 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import click
from races_helper import RaceHelper
import pandas as pd 
import time
import numpy as np 

# Return dog stats 
def get_dog_stats(dog, driver):
    url = "http://greyhoundbet.racingpost.com/" + dog[3]
    dog_page = get_code(url, driver, wait_type="id", wait_element="sortableTable")
    ratio_split, ratio_time, split, positions, weight, result = [],[],[],[],[], []
    stats, total, class_result = [], [], []
    arr_dt = []
    for tr_content in dog_page.find("table", {"id":"sortableTable"}).find_all("tr", class_="row")[:15]:
        try: 
            arr_dt = RaceHelper(tr_content.find_all("td")).array_data()
            if int(arr_dt[-1]) <= 2: arr_dt[-1] = 0
            if int(arr_dt[-1]) > 2: arr_dt[-1] = 1
            positions.append(arr_dt[2])
            weight.append(arr_dt[6])
            result.append(arr_dt[-1])
            ratio_time.append(round((arr_dt[4] - arr_dt[5])/arr_dt[5], 4))
            ratio_split.append(round((arr_dt[1] - (arr_dt[5]/5)) / (arr_dt[5]/5),4))            
            total.append(arr_dt)
        except Exception:
            pass 
       
    return stats 

# Return all links for dog results
def get_dogs_links(track, driver):
    page_html = get_code(
                    "http://greyhoundbet.racingpost.com/#{}".format(track), 
                    driver, 
                    wait_type="class", 
                    wait_element="result-dog-name-details")
    results = []
    for result in page_html.find_all("div", class_="container"):
        dog_name = result.find("div", class_="name").text.encode("utf-8")[2:-1]
        dog_place = int(result.find(
            "div", class_="place").text.encode(
            "utf-8")[2:-1].replace("st", "").replace("nd", "").replace("rd", "").replace("th", ""))
        dog_whelping = result.find("span", class_="dog-date-of-birth").text.encode("utf-8").replace(" ", "-")
        dog_page = result.find("a").attrs["href"].encode("utf-8")
        dog = [
            dog_name, dog_place, dog_whelping, dog_page
        ]
        results.append(dog)
    return results


# Return page code
def get_code(url, driver, wait_element=False, wait_type=False):
    if driver:
        driver.get(url)
        time.sleep(2)
        if wait_element and wait_type:
            if wait_type == "class": WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, wait_element)))
            if wait_type == "id": WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, wait_element)))
        return BeautifulSoup(driver.page_source, "html.parser")