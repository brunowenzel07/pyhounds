# --------------------------------------------------------
# Predict script
# --------------------------------------------------------

# Libraries
import click
import numpy as np


# Classes
import webdriver as webdriver
import tracks as t
import races  as r
import dogs   as d
import helper as hp
import database as db
# Initialization Objects
webdriver = webdriver.Webdriver(prefs=False,cache=False, headless=False)

# Click configurations
@click.command()
def predict():
    click.echo("--> Starting predict script...")
    tracks = t.Tracks(t_="predict")

    for future in tracks.future():
        race = r.Races(future, webdriver, "predict")
        infos = race.future_informations()
        print(infos)
        #stats = list()
        # # For each dog present in race, calculate the stats
        # for dog in race.future_dogs():
        #      dogs = d.Dogs(dog, infos, webdriver, "predict")
        #      s_ = dogs.stats()
        #      if len(s_) == 19:
        #          stats.append(np.append(s_, dog["trap"]))
        # hp.generated_predicts(stats, infos)

        


predict()
