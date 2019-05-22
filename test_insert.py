import api as connection
import datetime 
import json 

data = {
    "name": "Newcastle", 
    "time_label": "11:11", 
    "grade": "A4", 
    "distance": 480, 
    "time": "2019-05-22 11:11", 
    "dogs": [{
            "link": "#dog/race_id=1697052&r_date=2019-05-22&dog_id=517047",
            "trap": 1, 
            "name": "Geordie Zero ", 
            "comment": "Importance of a flier cannot be stressed enough",
            "probability": 83.43, 
            "best_time": 29.19
         }, 
         {
            "link": "#dog/race_id=1697052&r_date=2019-05-22&dog_id=523712",
            "trap": 2, 
            "name": "High St Brute ", 
            "comment": "Lacks course knowledge, that's a worrying fact",
            "probability": 15.8, 
            "best_time": 26.39}, 
         {
            "link": "#dog/race_id=1697052&r_date=2019-05-22&dog_id=515881",
            "trap": 3, 
            "name": "Moyar Charm ", 
            "comment": "Prefer to go with the 'devils' we know",
            "probability": 21.87, 
            "best_time": 25.91}, 
         {
            "link": "#dog/race_id=1697052&r_date=2019-05-22&dog_id=498413",
            "trap": 4, 
            "name": "Tullymurry Idaho ", 
            "comment": "No tales of the unexpected from this old 'un",
            "probability": 4.55, 
            "best_time": 27.67}, 
         {
            "link": "#dog/race_id=1697052&r_date=2019-05-22&dog_id=529639",
            "trap": 5, 
            "name": "Harton Jet ", 
            "comment": "Bound to improve for this further look at the track",
            "probability": 75.14, 
            "best_time": 25.47}, 
         {
            "link": "#dog/race_id=1697052&r_date=2019-05-22&dog_id=519745",
            "trap": 6, 
            "name": "Canny Raquel (W)", 
            "comment": "Expected to be around at the finish, include for sure",
            "probability": 62.21, 
            "best_time": 25.27}
         ]}

api = connection.API()
api.submit("tracks/add", data)
