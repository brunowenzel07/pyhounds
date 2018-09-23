import csv
from database import Database


db = Database("data/new_data_test.csv")
stats = []

with open("data/data_test.csv", "r") as csvfile:
    rows = csv.reader(csvfile)

    for row in rows:
        del(row[3])
        stats.append(row)

db.insert(stats)