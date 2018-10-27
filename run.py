# !/usr/bin/python 

import click 
import sys 
sys.path.insert(0, "functions/")
import train 
import predict 

@click.command()
@click.argument("script")
@click.option("--date")
@click.option("--a")
@click.option("--b")
@click.option("--url")

def main(url, a, b, script, date):
    if script == "train":
        train.run(date)
    elif script == "predict":
        predict.run(url, a, b)

if __name__ == "__main__":
    main()