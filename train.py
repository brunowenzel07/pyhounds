# --------------------------------------------------------
# Train script
# --------------------------------------------------------


# Libraries
import click

# Classes
import webdriver as webdriver
import results as res
import tracks as trks
import dogs as dg
from database import Database

# Initialization Objects
webdriver = webdriver.Webdriver(prefs=True, headless=True)

# Click configurations
@click.command()
@click.option("--date", help="Date to get results")
def train(date):

    db = Database("data/dataset.csv")
    results = res.Results(date, webdriver)
    for link in results.get_links():
        try:
            stats      = list()
            track      = trks.Track(link, webdriver)
            track_info = track.track_info()
            # dogs       = track.get_dogs()
            # for i, d_ in enumerate(dogs):
            #     dog  = dg.Dogs(d_, webdriver, track_info)
            #     s_   = dog.get_stats()
            #     if len(s_) != 0:
            #         stats.append(d_ + s_)
            # for i,s in enumerate(stats):
            #     for i,t in enumerate(stats):
            #         a_position = int(s[0])
            #         b_position = int(t[0])
            #         if a_position != b_position:
            #             row = [track_info[0]] + [track_info[3]] + [a_position] + [b_position] + s[4:] + t[4:]
            #             if a_position < b_position:
            #                 row.append("A")
            #             if b_position < a_position:
            #                 row.append("B")
            #             db.insert(row, "solo")
        except Exception as a:
            pass


train()
