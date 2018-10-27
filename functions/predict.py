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

def run(url, trap_a, trap_b):

    # Create a instance for webdriver 
    driver = webdriver.Chrome(chrome_options=chrome_options)

    # Create instance of classes
    helper, dogs, tracks = Helper(), Dogs(), Tracks()

    db = Database("data/data_train.csv")

    # Get track informations
    page_html = helper.get_page_code(url, driver, type_wait="class", element_wait="bigTrap")        
    track_stats = tracks.get_track_stats(page_html)

    stats, dogs_infos = [], []
    for dog in dogs.get_dogs(page_html,"predicts", a=trap_a, b=trap_b):
        try:            
            dog_page = dogs.get_page(dog,driver)
            dates = helper.get_dog_dates(dog_page, datetime.now())
            dog_stats = dogs.get_stats(dog, dog_page, dates)                    
            if len(dog_stats) > 0:
                stats.append(dog_stats)
                dogs_infos.append(dog)
        except Exception as a:
            print(a)
    driver.close()

    data_predict = [np.array(stats[0] + stats[1])]

       
    data_train, data_result = db.load()
        
    data = np.concatenate((data_train, data_predict), axis=0)        

    pca = PCA(n_components=4)
    scaler = StandardScaler()
    x_pca = pca.fit_transform(scaler.fit_transform(data))

    x_data = np.column_stack((x_pca[:,0][:-1], x_pca[:,2][:-1]))
    x_predict = np.column_stack((x_pca[:,0][-1], x_pca[:,2][-1]))

    clf = SVC(probability=True)
        
    clf.fit(x_data,np.ravel(data_result))

    pred, pred_proba = [int(clf.predict(x_predict)),clf.predict_proba(x_predict)]

    print("IA PREDICTION (%sv%s)" %(dogs_infos[0][3], dogs_infos[1][3]))
    print("%s - %s" % (track_stats[1], track_stats[0]))    
    print("Winner predict: [%s] %s" % (dogs_infos[pred][3],dogs_infos[pred][0]))
    print("Probability of Winner: %s" % round(pred_proba[0][pred] * 100, 6))
    print("Trap_A Comment: %s " % dogs_infos[0][1])
    print("Trap_B Comment: %s " % dogs_infos[1][1])
    print("Distance of Hyperplan: %s" % clf.decision_function(x_predict))

    plt.scatter(x_pca[:,0][:-1],x_pca[:,2][:-1], c=np.ravel(data_result))
    plt.scatter(x_pca[:,0][-1],x_pca[:,2][-1], c="black")
    plt.show()