#!/usr/bin/env python

import urllib.request
import base64
import mmh3
import json
import requests
import os

# get the env variables defined in the env file
envfile = open("/home/nburfield/Development/uptime/.envs")
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
    already_sent = None
    if os.path.exists('/home/nburfield/Development/uptime/processed.json'):
        sent_json_file = open('/home/nburfield/Development/uptime/processed.json')
        already_sent = json.load(sent_json_file)
        sent_json_file.close()

    with open('/home/nburfield/Development/uptime/saved.json') as json_file:
        data = json.load(json_file)
        if not already_sent:
            already_sent = {}

        for p in data:
            try:
                with urllib.request.urlopen(p) as response:
                    html = response.read()
                    encoded = base64.b64encode(html)
                    hashed = mmh3.hash128(encoded, 42, signed = True)

                    mark = True
                    if p in already_sent:
                        if already_sent[p]:
                            mark = False

                    if mark:
                        if data[p] != hashed:
                            email_message += "- Failed Hash for: " + str(p) + '\r\n'
                            already_sent[p] = True
            except:
                mark = True
                if p in already_sent:
                    if already_sent[p]:
                        mark = False
                if mark:
                    email_message += "- Failed EXCEPTION for: " + str(p) + '\r\n'
                    already_sent[p] = True

    if email_message != '':
        email_error(email_message, already_sent)

def email_error(message, mark_sent):
    try:
        requests.post("https://api.mailgun.net/v3/mg.bcinnovationsonline.com/messages",
                      auth=("api", envs['MAILGUN_KEY']),
                      data={"from": "BC Innovations <donotreply@bcinnovationsonline.com>",
                            "to": [envs['ALERT_EMAIL']],
                            "subject": "UpTime Alert",
                            "text": message})

        with open('/home/nburfield/Development/uptime/processed.json', 'w') as outfile:
            json.dump(mark_sent, outfile)

    except:
        pass

validate()
