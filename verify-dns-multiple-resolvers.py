#!/opt/epd/current/bin/python

import socket, dns.query, dns.zone, dns.resolver

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

