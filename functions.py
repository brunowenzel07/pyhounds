# -*- coding: UTF-8
# !/usr/bin/python 
import train as tr 
import predict as pred 
import tester as test 

def train(url):
    tr.run(url)
def predict(url):
    pred.run(url)
def tester(url):
    test.run(url)
