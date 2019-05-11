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

# Initialization Objects
webdriver = webdriver.Webdriver(prefs=True, headless=False)

# Click configurations
@click.command()
@click.option("--date", help="Date to get results")
def train(date):

    try:
        tracks = t.Tracks(date, webdriver)
        for link in tracks.links():
            race = r.Races(link, webdriver)
            infos = race.informations()
            for dog in race.dogs():
                print(dog)
                dogs = d.Dogs(dog, infos, webdriver)
                dogs.stats()
                break
            break

    except Exception as e:
        raise e
        webdriver.close()

    finally:
        webdriver.close()



train()
