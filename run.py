# -*- coding: UTF-8
# !/usr/bin/python 

# Import modules
import click 
import sys 
import functions
from multiprocessing import Process, Queue

@click.command()
@click.argument("script")
@click.option("--url")

def main(script, url):
    if script == "train":
        functions.train(url)
    elif script == "predict":
        functions.predict(url)
    elif script == "tester":
        functions.tester(url)
    else:        
        click.secho("Invalid option, see documentation.", bold=True, color="red")

if __name__ == "__main__":
    p = Process(target=main)
    p.start()
    p.join()