import urllib.request
import base64
import mmh3
import os
import datetime
import json


def rebuild():
    new_data = {}
    with open('saved.json') as json_file:  
        data = json.load(json_file)
        for p in data:
            with urllib.request.urlopen(p) as response:
                html = response.read()
                encoded = base64.b64encode(html)
                hashed = mmh3.hash128(encoded, 42, signed = True)
                new_data[p] = hashed

    ts = int(datetime.datetime.now().timestamp())
    os.rename("saved.json", "saved." + str(ts) + ".json")

    with open('saved.json', 'w') as outfile:  
        json.dump(new_data, outfile)


rebuild()
