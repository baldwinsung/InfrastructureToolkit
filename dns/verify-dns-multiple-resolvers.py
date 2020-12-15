#!/usr/bin/env python
#
# python2 requires pythondns 1.16
# pip install dnspython==1.16
#
# useful for querying multiple active directory servers also functioning as dns servers

import socket
import dns.query 
import dns.zone
import dns.resolver

# Basic query
#for rdata in dns.resolver.query('www.yahoo.com', 'CNAME') :
#    print rdata.target

# Set the DNS Server
resolver = dns.resolver.Resolver()
resolver.nameservers=[socket.gethostbyname('DC1')]
for rdata in resolver.query('HOST.BLAH.COM', 'CNAME') :
    print rdata.target

resolver = dns.resolver.Resolver()
resolver.nameservers=[socket.gethostbyname('DC2')]
for rdata in resolver.query('HOST.BLAH.COM', 'CNAME') :
    print rdata.target

resolver = dns.resolver.Resolver()
resolver.nameservers=[socket.gethostbyname('DC3')]
for rdata in resolver.query('HOST.BLAH.COM', 'CNAME') :
    print rdata.target

resolver = dns.resolver.Resolver()
resolver.nameservers=[socket.gethostbyname('DC3')]
for rdata in resolver.query('VIP.LB.BLAH.COM', 'A') :
    print rdata.target

