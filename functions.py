# -*- coding: UTF-8
# !/usr/bin/python 
import train as tr 
import predict as pred 

def train(url):    
    tr.run(url)

def predict(url, a, b):
    pred.run(url,a,b)

