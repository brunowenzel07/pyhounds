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
import api as connection 
import random 

# Initialization Objects
webdriver = webdriver.Webdriver(prefs=True,cache=True, headless=False)

# Click configurations
@click.command()
def predict():
    click.echo("--> Starting predict script...")
    tracks = t.Tracks(t_="predict")
    api = connection.API()

    for future in tracks.future():

        race = r.Races(future, webdriver, "predict")
        infos = race.future_informations()             
        infos["dogs"] = []
        stats = list()
        # For each dog present in race, calculate the stats
        for dog in race.future_dogs():            
            dogs = d.Dogs(dog, infos, webdriver, "predict")
            infos["w_track"], infos["w_trap"], infos["w_grade"] = dogs.extra_infos()
            dog["probability"] = round(random.uniform(1,99), 2)
            dog["best_time"]   = round(random.uniform(25,30), 2)
            dog.pop("date")
            infos["dogs"].append(dog)                
            
            s_ = dogs.stats()
            print(s_)
            if len(s_) == 19:
                stats.append(np.append(s_, dog["trap"]))
        hp.generated_predicts(stats, infos)
        break 

        

       # api.submit("tracks/add", infos)

        


predict()
