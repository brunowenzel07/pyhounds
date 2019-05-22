#
# Webdriver class
#
import click
from selenium import webdriver
from bs4 import BeautifulSoup

# Selenium webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


# Extra function
from time import sleep

class Webdriver:


    def __init__(self, cache=False, headless=False, prefs=False):

        click.echo("--> Loading Webdriver...")
        self.chrome_options = webdriver.ChromeOptions()
        if headless:
            self.chrome_options.add_argument("--headless")
        if cache:
            self.chrome_options.add_argument("user-data-dir=/home/acioli/cache")
        if prefs:
            self.prefs={
                "profile.managed_default_content_settings.images": 2,
                "profile.managed_default_content_settings.stylesheet": 2,
                'disk-cache-size': 5000
                }
            self.chrome_options.add_experimental_option('prefs', self.prefs)
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options)
        self.driver.minimize_window()

    def get(self, url, element_wait=False, type_element=False):
        # save main_window
        main_window = self.driver.current_window_handle
        # open new blank tab
        self.driver.execute_script("window.open();")
        # switch to the new window which is second in window_handles array
        self.driver.switch_to_window(self.driver.window_handles[1])
        # Get page_source
        self.driver.get(url)
        if element_wait and type_element:
            if type_element == "class":
                WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, element_wait)))
            elif type_element == "id":
                WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.ID, element_wait)))
            sleep(3)            
        bs4_page = BeautifulSoup(self.driver.page_source, "html.parser")
        self.driver.close()
        self.driver.switch_to_window(main_window)
        return bs4_page

    def close(self):
        self.driver.close()
