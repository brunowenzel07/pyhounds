# -*- coding: UTF-8
# !/usr/bin/python 

# Import modules
import click 
import sys 
import functions
from multiprocessing import Process, Queue

@click.command()
@click.argument("script")
@click.option("--year")
def main(script, year):
    for i in range(1,13):
        for j in range(1,30):
            url = "http://greyhoundbet.racingpost.com/#results-list/r_date=%s-%02d-%02d" % (year, i, j)
            if script == "train":
                functions.train(url)

if __name__ == "__main__":
    main()