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
@click.option("--url")
def main(script, date, url):    
    
    if script == "train":
        url = "http://greyhoundbet.racingpost.com/#results-list/r_date=%s" % date
        print("Accessing data from: %s" % url )
        functions.train(url)
    elif script == "predict":
        functions.predict(url)

if __name__ == "__main__":
    main()