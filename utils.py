# -*- coding: UTF-8
# !/usr/bin/python 
from requests import get
from bs4 import BeautifulSoup 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        dog_page = result.find("a").attrs["href"]
        dog = [
            dog_name, dog_place, dog_whelping, dog_page
        ]
        results.append(dog)
    return results
    
# Return page code
def get_code(url, driver, wait=False, wait_element=False, wait_type=False):
    if driver:
        driver.get(url)
        if wait_element and wait_type:
            if wait_type == "class": WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, wait_element)))
            if wait_type == "id": WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, wait_element)))
        return BeautifulSoup(driver.page_source, "html.parser")