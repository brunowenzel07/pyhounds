# !/usr/bin/python 
from helper import Helper
from selenium import webdriver


class Bot():

    def __init__(self):

        self.helper = Helper()
        self.driver = webdriver.Chrome()

    def get_dogs(self, type_):
        page_html = self.helper.diary_dogs(self.driver)
        
