# ------------------------------------------
# Helper functions
# ------------------------------------------

import numpy as np
import pandas as pd
import unicodedata

from sklearn.ensemble import RandomForestClassifier
from datetime import datetime
import re

features = ["5D",   "5T",  "5G",  "5PL",  "5PG",  "5B", "10D", "10T", "10G", "10PL", "10PG", "10B",
"15D", "15T", "15G", "15PL", "15PG", "15B", "LDR" ]

def card_url(url):
    return url
def form_url(url):
    print(url)

def generated_predicts(stats, infos):
    # Loading dataset
    df = pd.read_csv("data/dataset.csv", index_col=False)
    # drop nan values
    df.dropna(inplace=True)

    # Labellig results
    df["RESULT"] = df[["A_PLACE", "B_PLACE"]].apply(nl, axis=1)

    # Segment the dataet
    #df1 = df[(df["DISTANCE"] == infos["distance"]) & (df["TRACK"] == infos["track"]) & (df["GRADE"] == infos["grade"])]

    df1 = df[(df["DISTANCE"] == 450) & (df["TRACK"] == "Sunderland")]

    # Generated the newdataset
    X = pd.DataFrame(columns=features)
    for x_col in features:
        X[x_col] = df1[["A_"+x_col, "B_"+x_col]].apply(ns, axis=1)

    # Make classifier
    clf = RandomForestClassifier(n_estimators=100)
    clf.fit(X, df["RESULT"][X.index])

    # Voting for winners
    winners = []
    for i, s in enumerate(stats):
        probs_a = np.array([])
        probs_b = np.array([])
        for j, p in enumerate(stats):
            stats_a, stats_b = np.array(s[:-1]), np.array(p[:-1])
            trap_a, trap_b  = s[-1], p[-1]
            if trap_a != trap_b:
                X_pred = np.nan_to_num(stats_a/(stats_a + stats_b))
                prob_a, prob_b = clf.predict_proba([X_pred])[0]                
                probs_a = np.append(probs_a, prob_a)
                probs_b = np.append(probs_b, prob_b)
        winners.append({"trap" : trap_a, "mean" : np.mean(probs_a)})
        winners.append({"trap" : trap_b, "mean" : np.mean(probs_b)})
    print(winners)

def generated_stats(stats, infos):

    sss_ = list()
    for i, s in enumerate(stats):    
        s_copy = s.copy()
        trap_a, position_a = s.copy().pop("dog_trap"), s.copy().pop("dog_place")
        s_copy.pop("dog_trap")
        s_copy.pop("dog_place")    
        for j, t in enumerate(stats):
            t_copy = t.copy()
            trap_b, position_b = t.copy().pop("dog_trap"), t.copy().pop("dog_place")
            t_copy.pop("dog_trap")
            t_copy.pop("dog_place")    
            if position_a != position_b:            
                dog_a = np.array(list(s_copy.values()))
                dog_b = np.array(list(t_copy.values()))
                features = dog_a / (dog_a + dog_b)                
                features = list(np.round(np.nan_to_num(features).astype(float), 3))       
                features.append(trap_a)
                features.append(trap_b)
                if position_a < position_b:
                    result = "A"
                elif position_a > position_b:
                    result = "B"                
                features.append(result)
                features.append(infos["distance"])
                features.append(infos["grade"])                
                sss_.append(features)
    return sss_

def ns(s):
    s = np.array(s).astype(np.float)
    if s[0] == 0 or s[0] == s[1]:
        return 0.0
    else:
        return s[0] / (s[0] + s[1])
def nl(s):
    if int(s[0]) < int(s[1]):
        return "A"
    else:
        return "B"

def normalize(element, t_):
    """
        Title: Normalize function
        Description: parse texts elements and treats it.
    """
    try:
        if t_ == "text":
            return element.text
        if t_ == "date":
            s = element.text.replace(" ", "")
            return datetime.strptime(s, "%d%b%y")
        if t_ == "distance":
            return int(element.text.replace("m", ""))
        if t_ == "only_digits":
            return int(re.sub("\D", "", element.text))
        if t_ == "bends":
            element = element.text.replace("-", "")
            return np.average(np.array(list(element)).astype(int))
        if t_ == "remarks":
            return element.text.lower().split(",")
        if t_ == "float":
            return np.float(element.text)
        if t_ == "int":
            return np.int(element.text)
        if t_ == "by":            
            s = element.text
            if len(s) == 1:
                return float(s)
            elif len(s) == 2:
                return float(unicodedata.numeric(s[0])) * float(unicodedata.numeric(s[1]))
            elif len(s) > 2:
                try:
                    return float(s[:2]) * float(unicodedata.numeric(s[-1]))
                except Exception:
                    return 3
    except Exception:
        return float("NaN")