# -*- coding: UTF-8
# !/usr/bin/python 

from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re 
from datetime import datetime, timedelta
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import pandas as pd 

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
            trap = bs_element.attrs["class"][1].replace("trap","")
            return str(trap)
        if bs_type == "date_diff":
            today = datetime.now()
            dog = datetime.strptime(bs_element.text.encode("utf-8").replace(" ", ""), "%d%b%y")
            return float(((today - dog).days))

    def get_page_code(self, url, driver=False, element_wait=False, type_wait=False):
        if driver:
            driver.get(url)
            sleep(2)
            if type_wait == "class": WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, element_wait)))
            if type_wait == "id": WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, element_wait)))
        return BeautifulSoup(driver.page_source, "html.parser")

    def remarks_clf(self):
        train_df = pd.read_csv("data/comments.csv", header=None, names=["comment", "position"])
        # Bag of Words
        tfidf = TfidfTransformer()
        bow = CountVectorizer()
        bow.fit(train_df["comment"])
        # instanciando classificador
        nb = MultinomialNB(alpha=1.0)
        # treinamento, transformação do set de trainamento
        train_X_bow = bow.transform(train_df["comment"])
        tfidf.fit(train_X_bow)
        train_X_tfidf = tfidf.transform(train_X_bow)
        train_y = train_df["position"]
        nb.fit(train_X_tfidf, train_y)
        return [nb, bow, tfidf]

    def get_dog_data(self, dog_page):
        dog_age = dog_page.find("table",class_="pedigree").find_all("td")[3]
        dog_last_run = dog_page.find("table", {"id":"sortableTable"}).find_all("td", class_="c0")[0]
        last_run = self.normalize(dog_last_run, "date_diff") 
        dog_age = self.normalize(dog_age, "date_diff")
        return [dog_age, last_run]

    def count_unique(self, list_count, value_count):
        i, k = 0, 0
        for i in list_count:
            if i == value_count:
                k += 1 
        return k