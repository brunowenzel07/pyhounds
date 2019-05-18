# --------------------------------------------------------
# Predict script
# --------------------------------------------------------

# Libraries
import click

# Classes
import webdriver as webdriver
import tracks as t
import races  as r
import dogs   as d
import helper as hp
import database as db
# Initialization Objects
webdriver = webdriver.Webdriver(prefs=True, headless=False)

# Click configurations
@click.command()
def predict():
    click.echo("--> Starting predict script...")
    tracks = t.Tracks(t_="predict")
    for future in tracks.future():
        race = r.Races(future, webdriver, "predict")
        infos = race.informations()
        #print(infos)
        break


predict()
