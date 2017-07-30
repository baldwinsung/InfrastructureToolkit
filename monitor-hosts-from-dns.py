#!/usr/bin/python

import socket, string, os, re
import dns.query, dns.zone, dns.resolver

# Basic query
#for rdata in dns.resolver.query('www.yahoo.com', 'CNAME') :
#    print rdata.target

# Set the DNS Server
#resolver = dns.resolver.Resolver()
#resolver.nameservers=[socket.gethostbyname('ns1.cisco.com')]
#for rdata in resolver.query('www.yahoo.com', 'CNAME') :
#    print rdata.target

dns_server = '10.10.10.100'
dns_domain = 'blah.local'

z = dns.zone.from_xfr(dns.query.xfr(dns_server, dns_domain))
names = z.nodes.keys()
names.sort()

for n in names:
    #print z[n].to_text(n)
    host = str(n)
    host = host+"."+dns_domain
    try:
        p = os.system("ping -q -c 1 -W 2 " + host + " > /dev/null")
        if p == 0:
            print host, 'is up!'
            state = 'good'
        else:
            print host, 'is down!, check if record is stale'
    except:
        print "error"

dns_server = '10.10.10.100'
zone_pre   = '10.10'
zone_post  = 'in-addr.arpa'
zone_rev   = re.split("\.", zone_pre)
dns_rev    = zone_pre+ '.' +zone_post

z = dns.zone.from_xfr(dns.query.xfr(dns_server, dns_rev))
names = z.nodes.keys()
names.sort()

for n in names:
    #print z[n].to_text(n)
    host = str(n)
    rev_host = re.split("\.", host)
    if len(rev_host) == 2:
        new_host = zone_rev[1]+ "." +zone_rev[0]+ "." +rev_host[1]+ "." +rev_host[0]
        try:
            p = os.system("ping -q -c 1 -W 2 " + new_host + " > /dev/null")
            if p == 0:
                #print host, 'is up!'
                state = 'good'
            else:
                print new_host, 'is down!, check if record is stale'
        except:
            print "error"
