# --------------------------------------------------------
# Train script
# --------------------------------------------------------

# Libraries
import click
import numpy as np
import pprint

# Classes
import webdriver as webdriver
import tracks as t
import races  as r
import dogs   as d
import helper as hp
import database as db
# Initialization Objects
webdriver = webdriver.Webdriver(prefs=True, headless=False, type_="train")

# Click configurations
@click.command()
@click.option("--date", help="Date to get results")
def train(date):

    dataB = db.Database("data/dataset.csv")

    try:

        # Initialization of tracks classes
        tracks = t.Tracks(link=date,driver=webdriver, t_="train")

        # loop throught the page links
        for i, link in enumerate(tracks.links()):
            click.echo("--> [%s] Accessing the url: %s" % (i, link))
            # Initialization of races classe
            race       = r.Races(link=link, driver=webdriver, t_="train")
            # getting infos of race
            infos      = race.train_informations()
            # Declare a list that contain all stats of dog's race
            stats = list()
            # For each dog present in race, calculate the stats
            for dog in race.train_dogs():
                s_ = {}
                print(infos)
                try:
                    dd = d.Dogs(dog, infos, webdriver, "train")
                    s_ = dd.stats()
                    s_["trap"]     = dog["trap"]
                    s_["place"]    = dog["place"]
                    stats.append(s_)
                except Exception:
                    click.secho("--> Error while getting dog data")
            rows = hp.generated_stats(stats, infos)
            dataB.insert(rows, "multiple")
    except Exception as e:
        raise e
        webdriver.close()

    finally:
        webdriver.close()



train()
