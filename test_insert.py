import api as connection
import datetime 
import json 

data = {
    "name" : "Perry Barr",
    "time" : "2019-05-23 16:09:00",
    "distance" : 450,
    "time_label" : "16:09",
    "grade" : "A3"
}

api = connection.API()
api.submit("tracks/add", data)
