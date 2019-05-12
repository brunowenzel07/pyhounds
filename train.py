# --------------------------------------------------------
# Train script
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
webdriver = webdriver.Webdriver(prefs=True, headless=True)

# Click configurations
@click.command()
@click.option("--date", help="Date to get results")
def train(date):

    dataB = db.Database("data/dataset.csv")

    try:

        # Initialization of tracks classes
        tracks = t.Tracks(date, webdriver)

        # loop throught the page links
        for i, link in enumerate(tracks.links()):
            click.echo("--> [%s] Accessing the url: %s" % (i, link))
            # Initialization of races classe
            race       = r.Races(link, webdriver)
            # getting infos of race
            infos      = race.informations()
            # Declare a list that contain all stats of dog's race
            stats = list()
            # For each dog present in race, calculate the stats
            for dog in race.dogs():
                 dogs = d.Dogs(dog, infos, webdriver)
                 s_ = dogs.stats()
                 if len(s_) == 21:
                     stats.append(s_)

            dogs_stats = hp.generated_stats(infos, stats)

            dataB.insert(dogs_stats, "multiple")


    except Exception as e:
        raise e
        webdriver.close()

    finally:
        webdriver.close()



train()
