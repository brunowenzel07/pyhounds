#-*- coding: UTF-8
#!/usr/bin/python 

import csv 
import pandas as pd 
import numpy as np 
a = []

with open("data/txt_comments.csv", "r") as csvfile:
    rows =csv.reader(csvfile)
    for row in rows:
        for i in row:
            a.append(i)


c, d = np.unique(a, return_counts=True)


 
for p in c:
    with open("data/comments.csv", "a") as csvcomments:
        writer = csv.writer(csvcomments)   
        writer.writerow(str(p))
        