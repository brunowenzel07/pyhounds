# -*- coding: UTF-8
# !/usr/bin/python 

# Import modules
import click 
import sys 
import functions
from database import Database

@click.command()
@click.argument("script")
@click.option("--date")
@click.option("--url")
@click.option("--a")
@click.option("--b")
@click.option("--type_run")
@click.option("--m")


def main(script, date, url, a, b, type_run, m):    
   
    if script == "train":
        if (type_run):
            for j in range(1,30):                
                date = "2018-%s-%02d"% (m, j)                    
                #url = "http://greyhoundbet.racingpost.com/#results-list/r_date=%s" % date
                #print("Accessing data from: %s" % url )
                #functions.train(url)
                Database("data/dates.csv").insert([date], "solo")

    elif script == "predict":
        functions.predict(url, a, b)


if __name__ == "__main__":
    main()