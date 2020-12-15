#!/usr/bin/env python

import ldap, re, sys, string, Sybase, socket, os, syslog, xmlrpclib, re

#if len(sys.argv) != 2:
#        print "Usage: $0 <hostname>"
#        sys.exit(1)

#bldap_host = sys.argv[1]

### FUNCTIONS


### ROUTINES FOR TCP CHECK
def btcpcheck ( searchhost ):
	host = searchhost
	port = 22
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(2)
	try:
	#	print host
		s.connect((host, port))
		s.shutdown(1)
	#	print searchhost+ " ssh is listening "
	except:
		print searchhost+ " ssh is NOT listening - box is down - please check thank you\n"
		syslog.syslog(syslog.LOG_ERR, searchhost+ " ssh is NOT listening - box is down - please check thank you\n")


### ROUTINES FOR DNS
def bdnscheck ( searchhost ):
	host = searchhost
	try:    
		s = socket.gethostbyname(host)    
		#print s
	except socket.gaierror, err:  
		print searchhost+ " is NOT in DNS - please check thank you\n"
                syslog.syslog(syslog.LOG_ERR, searchhost+ " is NOT in DNS - please check thank you\n")

### ROUTINES FOR SYBASE SEARCH
def bsybase( searchhost ):

	database_hn	= 'PROD'
	database_un	= 'username'
	database_pw	= 'password'
	database_db	= 'inventory'
	db = Sybase.connect(database_hn, database_un, database_pw, database_db)
	c = db.cursor()
	c.execute('select dev.hostname, dev.device_type, dep.name, tu.first_name, tu.last_name, tu.smtp_address, dev.notes from inventory..device as dev, common.dbo.department as dep, common.dbo.BLAH_user as tu' 
		  ### DEPT MUST BE DEFINED
		  ' where dev.BLAH_user_id = tu.BLAH_user_id and tu.department_id = dep.department_id and dev.is_active = "1"' 
		  ' and lower(dev.hostname) = @sh', {'@sh': searchhost} )
		  ### SPECIFIC
		  #' and lower(dev.hostname) = "admin1-location" ')
    	#print string.join([row[0] for row in c.fetchall()], '')
	rows = c.fetchall()

	if rows:
		for row in rows:
			inv_host  = row[0]
 			inv_team  = row[2]
 			inv_env   = "not def in db"
 			inv_os    = row[1]
			inv_osver = "not def in db"
			inv_owner = row[3],row[4]
	else:
		print searchhost+ " not in sybase inventory check dept and owner, did you add to inventory after kickstarting or jumpstarting?\n"
		syslog.syslog(syslog.LOG_ERR, searchhost+ " not in sybase inventory check dept and owner, did you add to inventory after kickstarting or jumpstarting?\n")

### ROUTINES FOR LDAP SEARCH AND INITIAL POPULATION OF DESCRIPTIONS
#def bldap( searchhost ):
def bldap():
	ldap_server 	= 'SERVER.SUB.BLAH.com' 
	base_dn 	= 'ou=unix-servers,ou=unix,DC=SUB,DC=BLAH,DC=com' 
	username 	= 'cn=S-SERVICEACCOUNT,ou=ServiceAccounts,ou=People,ou=Admins,DC=SUB,DC=BLAH,DC=com' 
	password	= 'PASSWORD' 
	filter    	= "(objectclass=computer)" 
	attributes 	= ['name','operatingSystem','operatingSystemVersion','description']

	l = ldap.initialize('ldap://SUB.BLAH.com:389')
	l.simple_bind_s(username, password)
	r = l.search_s(base_dn,ldap.SCOPE_SUBTREE,filter,attributes)
	r = sorted(r,reverse=True)

	for dn,entry in r:
		# debug
		#print '%s | %s' % (dn, entry['name'][0])
		
		# find environment via ou listed in dn
		DD    = dn
		host  = DD.split(",")[0]
		host  = re.sub("CN=", "", host)
		host  = host.lstrip()
		host  = host.rstrip()
		env   = DD.split(",")[1]
		env   = re.sub("OU=", "", env)
		team  = DD.split(",")[2]
		team  = re.sub("OU=", "", team)
		#print '%s %s %s' % (host, env, team)
		
		# initial population update description to Owner: NOT_DEFINED
		#mod_attrs = [( ldap.MOD_REPLACE, 'Description', 'Owner: NOT_DEFINED' )]
		#l.modify_s(dn, mod_attrs)
		
		# get os osver owner-via-description
		#if host == entry['name'][0]:
		#print DD
		#print host
		osver = entry['operatingSystemVersion'][0]
		os    = entry['operatingSystem'][0]
		#owner = entry['description'][0]
		
		#if searchhost == host:
			#print "%s is an %s machine in %s running %s %s %s" % (host, team, env, os, osver, owner)
		#print "%s is an %s machine in %s running %s %s %s" % (host, team, env, os, osver, owner)
		#print "%s, %s %s" % (host, os, osver)
		#print "%s, %s " % (host, os)
		
		### opt cross reference machine with inventorydb sybase
		bsybase ( host )

		### check if host is pingable
		btcpcheck ( host )
		
		### check if host is in dns
		bdnscheck ( host )

		# opt check disk usage, host uptime, host load average via snmp

def bsat():
 
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
		bsybase ( host )
		btcpcheck ( host )
		bdnscheck ( host )
	client.auth.logout(key)


### MAIN
#bldap( bldap_host )
bldap()
bsat()

