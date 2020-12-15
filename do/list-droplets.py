#!/usr/bin/env python
import requests, json

accessToken = "TOKEN"
url         = "https://api.digitalocean.com/v2/droplets"
headers     = {"Authorization": "Bearer "+accessToken}

r           = requests.get(url, headers=headers)

return_code = str(r.status_code)
#print ( return_code )
results     = r.json()
#print (json.dumps(results, indent=2))

for machine in results['droplets']:
    hostname  = machine['name']
    ipaddress = machine['networks']['v4'][0]['ip_address']

    print hostname, ipaddress
