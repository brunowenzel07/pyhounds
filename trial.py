import csv 

with open("data/data_train.csv", "r") as csv1:
    rows = csv.reader(csv1)
    i = 0
    for r in rows:
        if "inf" in r:
            i = i+1
        else:
            with open("data/train.csv", "a") as csv2:
                csv.writer(csv2).writerow(r)
print(i)