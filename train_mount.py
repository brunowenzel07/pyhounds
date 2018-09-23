import click 
import functions 

p = 0
for i in range(1,9):
    for j in range(1,30):
        url = "http://greyhoundbet.racingpost.com/#results-list/r_date=2018-%02d-%02d" % (i, j)
        functions.train(url)
        p += 1
        if p == 10000: break 