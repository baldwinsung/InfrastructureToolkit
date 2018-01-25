#!/usr/bin/python
import requests, json

accessToken = "TOKEN"
url         = "https://api.digitalocean.com/v2/firewalls"
headers     = {"Authorization": "Bearer "+accessToken}

r           = requests.get(url, headers=headers)

return_code = str(r.status_code)
#print ( return_code )
results     = r.json()
#print (json.dumps(results, indent=2))

for rule in results['firewalls']:
    name                = rule['name']
    inbound_source_addy = rule['inbound_rules'][0]['sources']['addresses'][0]
    
    print name, inbound_source_addy
    #print inbound_source_addy


