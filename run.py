# !/usr/bin/python 

import click 
import sys 
sys.path.insert(0, "functions/")
import train 

@click.command()
@click.argument("script")
@click.option("--date")
@click.option("--type_run")
@click.option("--a")
@click.option("--b")
@click.option("--url")


def main(script, date, type_run, a, b, url):
        if script == "train":
                train.run(date)
        elif script == "predict":
                predict.run(url, trap_a, trap_b)


if __name__ == "__main__":
    main()