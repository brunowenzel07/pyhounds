# -*- coding: UTF-8
# !/usr/bin/python 

# Import modules
import click 
import sys 
import functions
from multiprocessing import Process, Queue

@click.command()
@click.argument("script")
@click.option("--date")
def main(script, date):
    url = "http://greyhoundbet.racingpost.com/#results-list/r_date=%s" % date
    print("Accessing data from: %s" % url )
    if script == "train":
        functions.train(url)

if __name__ == "__main__":
    main()