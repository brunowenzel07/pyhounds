# !/usr/bin/python 
import sys 
from selenium import webdriver 
import click 
from datetime import datetime 
import numpy as np 

sys.path.insert(0, "classes/")
from tracks import Tracks
from helper import Helper
from dogs import Dogs 
from database import Database
import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt 
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler

# Define options for the headless browser 
chrome_options = webdriver.ChromeOptions()
prefs={
    "profile.managed_default_content_settings.images": 2, 
    "profile.managed_default_content_settings.stylesheet": 2, 
    'disk-cache-size': 8192 
    }
chrome_options.add_experimental_option('prefs', prefs)
names = [
    "d1_bends_mean",
    "d1_bends_std",
    "d1_split_mean",
    "d1_split_std",
    "d1_posit_mean",
    "d1_posit_std",
    "d2_bends_mean",
    "d2_bends_std",
    "d2_split_mean",
    "d2_split_std",
    "d2_posit_mean",
    "d2_posit_std",
    "class"
]
def run():

    # Create a instance for webdriver 
    #driver = webdriver.Chrome(chrome_options=chrome_options)

    # Create instance of classes
    helper, dogs, tracks = Helper(), Dogs(), Tracks()

    db = Database("data/data_train.csv")

   
       
    data_train = db.load()      
    

    data = pd.DataFrame(data_train, columns=names)    

    print(data.head())

    pca = PCA(n_components=4)
    scaler = StandardScaler()
    scaled_x = scaler.fit_transform(data.drop([
        "d1_posit_mean", 
        "d1_bends_mean", 
        "d1_split_mean", 
        "d2_posit_mean", 
        "d2_bends_mean", 
        "d2_split_mean"], axis=1))
    print(scaled_x.shape)
    x_pca = pca.fit_transform(scaled_x)
    print(x_pca)

if __name__ == "__main__":
    run()