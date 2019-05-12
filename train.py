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

# Initialization Objects
webdriver = webdriver.Webdriver(prefs=True, headless=False)

# Click configurations
@click.command()
@click.option("--date", help="Date to get results")
def train(date):

    try:

        # Initialization of tracks classes
        tracks = t.Tracks(date, webdriver)

        # loop throught the page links
        for link in tracks.links():
            click.echo("--> Accessing the url: %s" % link)
            # Initialization of races classe
            race       = r.Races(link, webdriver)
            # getting infos of race
            infos      = race.informations()
            # Declare a list that contain all stats of dog's race
            stats = list()
            # For each dog present in race, calculate the stats
            for dog in race.dogs():
                 dogs = d.Dogs(dog, infos, webdriver)
                 stats.append(dogs.stats())

            stats = hp.generated_stats(infos, stats)

            break

    except Exception as e:
        raise e
        webdriver.close()

    finally:
        webdriver.close()



train()
