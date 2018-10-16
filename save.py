import csv 
import numpy as np 
from sklearn.preprocessing import Normalizer
from database import Database
import seaborn as sns 
import pandas as pd
import matplotlib.pyplot as plt 




races = pd.read_csv("data/data_train.csv",names=[
    "d1_bends",
    "d1_remarks",
    "d1_top1",
    "d1_top2",
    "d1_top3",
    "d1_gng",
    "d1_weight",
    "d1_split",
    "d1_whelping",
    "d1_last_run"
    "d2_bends",
    "d2_remarks",
    "d2_top1",
    "d2_top2",
    "d2_top3",
    "d2_gng",
    "d2_weight",
    "d2_split",
    "d2_whelping",
    "d2_last_run",
    "result"
])


print(races["d1_weight"].head(10).mean())