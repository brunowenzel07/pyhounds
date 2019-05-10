#
# helper functions
#

import numpy as np

def frame_percent(df, col, position):
    return len(df[df[col].astype(np.float) == position]) / len(df)

def avg_bends(data):
    return np.average(np.array(data).astype(np.int))

def std(s):
    if s[0] == 0 or s[0] == s[1]:
        return 0.0
    else:
        return s[0] / (s[0] + s[1])

def avg_bends(self, data):
    return np.average(np.array(data).astype(np.int))

def normalize(bs_element, t_):
    if t_ == "sp":
        if len(bs_element) == 2:
            e_ = list()
            for b in bs_element:
                e_.append(float(re.sub("\D", "", b)))
            return e_[0] / e_[1]
        else:
            return float("NaN")
    if t_ == "split":
        if len(bs_element) != 0:
            return float(bs_element)
        else:
            return float("NaN")
    if t_ == "gng":
        if len(bs_element) > 1:
            return float(bs_element)
        else:
            return 0
