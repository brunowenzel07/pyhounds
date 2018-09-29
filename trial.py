#-*- coding: UTF-8
#!/usr/bin/python 

with open('data/data_train.csv','r') as in_file, open('data/new_data.csv','w') as out_file:
    seen = set() # set for fast O(1) amortized lookup
    for line in in_file:
        if line not in seen: 
            seen.add(line)
            out_file.write(line)