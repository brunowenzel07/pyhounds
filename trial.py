import csv 
from database import Database

db = Database("data/avb.csv")

with open("data/data_train.csv", "r") as csv1:
    rows = csv.reader(csv1)
    q, i = 0, 0
    stats = []
    for r in rows:
        q += 1 
        del r[-1]
        stats.append(r)
        if q == 6:  
     

            for i, s in enumerate(stats):
                for k, t in enumerate(stats):
                    a_position = int(s[-1])
                    b_position = int(t[-1])
                    if a_position == 1 and b_position == 6:
                        row = s[:-1] + t[:-1] + [0]
                        db.insert(row, "solo")                    
                    elif a_position == 5 and b_position == 2:
                        row = s[:-1] + t[:-1] + [1]
                        db.insert(row, "solo")
                    
            q = 0
            stats = []             
                   