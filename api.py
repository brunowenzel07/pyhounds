# API script 

import requests 
import json 

class API:

    def __init__(self, url = "http://localhost/greyhounds/", port=80):
        self.url  = url 
        self.port = port 

    def submit(self, endpoint, data):        
        r = requests.post(url=self.url+endpoint, data = data)
        print(r.text)