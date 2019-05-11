# --------------------------------------------------------
# Train script
# --------------------------------------------------------


# Libraries
import click

# Classes
import webdriver as webdriver
import tracks as tracks 

# Initialization Objects
webdriver = webdriver.Webdriver(prefs=True, headless=True)

# Click configurations
@click.command()
@click.option("--date", help="Date to get results")
def train(date):



train()
