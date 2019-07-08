import urllib.request
import base64
import mmh3
import json
import requests

# get the env variables defined in the env file
envfile = open(".envs")
envs = {}
for line in envfile:
  linesplit = line.split(':')
  try:
    if linesplit[0].strip()[0] != '#':
      envs.update({linesplit[0].strip(): linesplit[1].strip()})
  except:
    pass

def validate():
    email_message = ''    
    with open('saved.json') as json_file:
        data = json.load(json_file)
        for p in data:
            with urllib.request.urlopen(p) as response:
                html = response.read()
                encoded = base64.b64encode(html)
                hashed = mmh3.hash128(encoded, 42, signed = True)

                if data[p] != hashed:
                    email_message += "- Failed Hash for: " + str(p) + '\r\n'
                else:
                    email_message += "+ Successful Hash for: " + str(p) + '\r\n'

    if email_message != '':
        email_error(email_message)

def email_error(message):
    requests.post("https://api.mailgun.net/v3/mg.billcookecreative.com/messages",
                  auth=("api", envs['MAILGUN_KEY']),
                  data={"from": "Bill Cooke Creative <donotreply@mg.billcookecreative.com>",
                        "to": [envs['ALERT_EMAIL']],
                        "subject": "UpTime Alert",
                        "text": message})

validate()
