#
# train script
#

# Libraries
import click 
from selenium import webdriver 



# Classes
import results
from database import Database
import predicts as pred
import pandas as pd 
import numpy as np 

click.echo("--> Loading inital conditions...")
# Selenium webdriver configurations 
# Define options for the headless browser 
chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument("user-data-dir=/home/acioli/cache")
prefs={
    "profile.managed_default_content_settings.images": 2, 
    "profile.managed_default_content_settings.stylesheet": 2, 
    'disk-cache-size': 1024
    }
chrome_options.add_experimental_option('prefs', prefs)
#chrome_options.add_argument("--headless")
click.echo("--> Loading selenium webdriver...")
driver = webdriver.Chrome(chrome_options=chrome_options)


# Click configurations
@click.command()
@click.option("--trap_a", help="Dog in trap a")
@click.option("--trap_b", help="Dog in trap b")
@click.option("--url", help="Race urlcl")

def predict(trap_a, trap_b, url):    
    click.echo("--> Requesting links of results...")    
    p = pred.Predicts(driver, url, trap_a, trap_b)    
    dogs = p.get_dogs()
    infos = p.get_race_infos()

    stats = list()
    for dog in dogs:
        s_ = p.get_dog_stats(dog, infos)
        if int(dog[-1]) == int(trap_a):
            sa = np.array(s_)
        if int(dog[-1]) == int(trap_b):
            sb = np.array(s_)
    t = sa / (sa + sb)
    t = np.nan_to_num(t)    
    y_pred = p.predict([t])

    

    driver.close()


# Run script only main menu
if __name__ == "__main__":
    predict()