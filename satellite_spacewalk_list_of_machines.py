#!/usr/bin/python
import xmlrpclib, re
 
SATELLITE_URL      = "http://SAT-SERVER.BLAH.COM/rpc/api"
SATELLITE_LOGIN    = "LOGIN"
SATELLITE_PASSWORD = "PASSWORD"
 
client = xmlrpclib.Server(SATELLITE_URL, verbose=0)
key = client.auth.login(SATELLITE_LOGIN, SATELLITE_PASSWORD)

list = client.system.listSystems(key)
for box in list:
    #print box.get('name')
    host = box.get('name')
    if "SUB.BLAH.COM" in host:
        host = re.sub('\.SUB.BLAH.COM$', '', host)
        
    print host

client.auth.logout(key)
