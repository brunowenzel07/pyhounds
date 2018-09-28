# -*- coding: UTF-8
# !/usr/bin/python 

from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re 
from datetime import datetime 

class Helper:

    def __init__(self):
        pass

    def normalize(self, bs_element, bs_type):
        if bs_type == "float":
            return float(bs_element.text.encode("utf-8"))
        if bs_type == "int":
            return int(bs_element.text.encode("utf-8"))
        if bs_type == "string":
            return str(bs_element.text.encode("utf-8"))
        if bs_type == "only_digits":
            return re.sub("\D", "", bs_element.text.encode("utf-8").replace(" ", ""))
        if bs_type == "link":
            return str(bs_element.attrs["href"].encode("utf-8"))
        if bs_type == "whelping":
            string = bs_element.text.encode("utf-8").replace(" ", "")
            whelping_date = datetime.strptime(string, "%d%b%y")
            today = datetime.now()
            age_dog = (today) - (whelping_date)
            return (age_dog.days)/30
        if bs_type == "brt":
            print(bs_element)
            element = bs_element.text.encode("utf-8")
            element = element.replace("BRT: ", "")
            element = element[:5]
            return float(element)
        if bs_type == "trap":
            trap = "cu"
            trap = bs_element.attrs["class"][1].replace("trap","")
            return str(trap)


    def get_page_code(self, url, driver=False, element_wait=False, type_wait=False):
        if driver:
            driver.get(url)
            if type_wait == "class": WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, element_wait)))
            if type_wait == "id": WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, element_wait)))
        return BeautifulSoup(driver.page_source, "html.parser")