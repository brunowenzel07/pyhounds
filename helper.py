# ------------------------------------------
# Helper functions
# ------------------------------------------

import numpy as np
from datetime import datetime
import re

def generated_stats(infos, stats):

    stats = list()
    for i, s in enumerate(stats):
        for j, t in enumerate(stats):
            a_position, a_trap = s[-2], s[-1]
            b_position, b_trap = t[-2], t[-1]
            if a_position != b_position:
                row = infos + list(s) + list(t)
                if a_position < b_position:
                    row.append("A")
                elif a_position > b_position:
                    row.append("B")
                stats.append(row)




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
    except Exception as e:
        return float("NaN")
