#
# train script
#

# Libraries
import click 
from selenium import webdriver 

# Classes
import results
from database import Database

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
@click.option("--date", help="Date to get results")

def train(date):

    db = Database("data/dataset.csv")
    click.echo("--> Requesting links of results...")
    res = results.Results(date,driver)    
    for link in res.get_links():
        stats = list()
        race_infos = res.get_race_infos(link)
        dogs = res.get_dogs(link)
        for i, dog in enumerate(dogs):        
            try: 
                s_ = res.get_dog_stats(dog, race_infos)
                if len(s_) != 0:
                    stats.append(s_)
            except Exception as a:
                print(a)

        for i,s in enumerate(stats):
            for i,t in enumerate(stats):
                a_position = int(s[0])
                b_position = int(t[0])
                if a_position != b_position:
                    row = s[3:] + t[3:]
                    row.append(a_position)
                    row.append(b_position)
                    if a_position == 1 and b_position > a_position:
                        print("A", a_position, b_position)
                        row.append("A")
                        db.insert(row, "solo")
                    if a_position == len(stats) and b_position < a_position:
                        print("B", a_position, b_position)
                        row.append("B")
                        db.insert(row, "solo")
    driver.close()















# Run script only main menu
if __name__ == "__main__":
    train()