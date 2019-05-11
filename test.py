import click 

click.echo("--> Loading libraries.. ")
import numpy as np 
import pandas as pd 
import time 
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
import dogs as dg 
import predicts as pred
from bs4 import BeautifulSoup
from time import sleep

# ---------------------------
# Extra functions
# ---------------------------
def normalize(s):
    if s[0] == 0 or s[0] == s[1]:
        return 0.0
    else:
        return s[0] / (s[0] + s[1])

# ---------------------------
# Features names
# ---------------------------
names = [
    "DA_TY_1", "DA_TY_2", "DA_TY_3", "DA_TY_4","DA_LY_1", "DA_LY_2", "DA_LY_3", "DA_LY_4","DA_T3_TMIN"  , "DA_T3_TMEAN","DA_T3_BENDS" , "DA_T3_FIN",
    "DA_T12_TMIN" , "DA_T12_TMEAN","DA_T12_BENDS", "DA_T12_FIN","DB_TY_1", "DB_TY_2", "DB_TY_3", "DB_TY_4", "DB_LY_1", "DB_LY_2", "DB_LY_3", "DB_LY_4",    
    "DB_T3_TMIN"  , "DB_T3_TMEAN","DB_T3_BENDS" , "DB_T3_FIN","DB_T12_TMIN" , "DB_T12_TMEAN","DB_T12_BENDS", "DB_T12_FIN","A_POS", "B_POS", "RES"
    ]
features = [
    "TY_1", "TY_4", "LY_1", "LY_4", "T3_TMIN"  , "T3_TMEAN", "T3_BENDS" , "T3_FIN", "T12_TMIN" , "T12_TMEAN",
    "T12_BENDS", "T12_FIN"
    ]

# -------------------------------------
# Selenium webdriver configurations 
# -------------------------------------
click.echo("--> Loading selenium webdriver...")
chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument("user-data-dir=/home/acioli/cache")
prefs={
    "profile.managed_default_content_settings.images": 2, 
    "profile.managed_default_content_settings.stylesheet": 2, 
    'disk-cache-size': 1024
    }
chrome_options.add_experimental_option('prefs', prefs)
#chrome_options.add_argument("--headless")



# -------------------------------------
# Dataset
# -------------------------------------
def weight(data):
    data = np.array(data)
    return np.log(data[1]/data[0]) ** 2
click.echo("--> Loading dataset..")
df = pd.read_csv("data/dataset.csv", names=names)
comments = pd.read_csv("data/comments.csv")
df.dropna(inplace=True)
df.drop_duplicates(keep = False, inplace = True)
click.echo("--> Pre-processing dataset...")
df["W"] = df[["A_POS", "B_POS"]].apply(weight, axis=1)
X = pd.DataFrame(columns=features)
for x_col in features:
    X[x_col] = df[["DA_"+x_col, "DB_"+x_col]].apply(normalize, axis=1)

# -------------------------------------
# Enrivonment
# -------------------------------------
click.echo("--> Training classifier... ")
c = True
j = True

gbc = GradientBoostingClassifier(n_estimators=50, min_samples_leaf=20)
rfc = RandomForestClassifier(n_estimators=50, min_samples_leaf=100)
gbc.fit(X, df["RES"], sample_weight=df["W"][X.index.values])
rfc.fit(X, df["RES"], sample_weight=df["W"][X.index.values])

while c != False:

    # user interation
    
    click.clear()
    stats = list()
    click.echo("---> New predict <--")
    url = click.prompt('---> URL')
    j = True
    while j:
        driver = webdriver.Chrome(chrome_options=chrome_options)
        trap_a = click.prompt('---> Trap A')
        trap_b = click.prompt('---> Trap B')        
        click.echo("---> Loading result page...")
        driver.get(url)
        sleep(4)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "cardTabContainer")))
        page = BeautifulSoup(driver.page_source, "html.parser")
        click.echo("---> Create instance of dogs class..")    
        d = dg.Dogs(driver, url, trap_a, trap_b, page)    
        infos = d.get_race_infos()        
        dd = d.get_dogs()
        traps_a, traps_b, freq_a, freq_b = [], [], [], []
        for dog in dd:
            s_, freq, traps = d.get_dog_stats(dog, infos)
            if int(dog[-1]) == int(trap_a):
                sa = np.array(s_)
                ssa = dog
                freq_a = freq 
                traps_a = traps                 
            if int(dog[-1]) == int(trap_b):                
                sb = np.array(s_)
                ssb = dog                                
                freq_b = freq                 
                traps_b = traps 
        try:
            t = sa / (sa + sb)
            t = np.nan_to_num(t)    
            click.clear()       
            rfc_pred = rfc.predict_proba([t])
            gbc_pred = gbc.predict_proba([t]) 
            click.echo("-----------------------------------------------")
            click.echo("---> Predição de resultados AvB")
            click.echo("---> Informações da Track: %s - %s (%sm)" % (infos[-1], infos[1], infos[0]))            
            click.echo("---> Trap %s: %s - Probabilidade: %0.2f%s" % (ssa[-1], ssa[0], (100 * np.average([rfc_pred[0][0], gbc_pred[0][0]])), "%"))
            click.echo("---> Trap Preferida: [%s]" % int(traps_a))
            ca = list()
            for i in freq_a:
                if i in comments.rmk.values:
                    ca.append(comments[comments["rmk"] == i].values[0][1])            
            click.echo("---> Comentários: %s " % ", ".join(ca))            
            click.echo("---> Trap %s: %s - Probabilidade: %0.2f%s" % (ssb[-1], ssb[0], (100 * np.average([rfc_pred[0][1], gbc_pred[0][1]])), "%"))
            click.echo("---> Trap Preferida: [%s]" % int(traps_b))
            cb = list()
            for i in freq_b:
                if i in comments.rmk.values:
                    cb.append(comments[comments["rmk"] == i].values[0][1])            
            click.echo("---> Comentários: %s " % ", ".join(cb))

            
        except Exception as a:
            print(a)
            click.secho("---> Data corrupt!", fg="red")

        driver.close()
        j = click.confirm('---> Another prediction in this url?')
    c = click.confirm('--> Do you want to continue predictions?')
driver.close()