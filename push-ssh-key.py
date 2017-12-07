#!/usr/bin/python

# Script based off example on http://pexpect.readthedocs.io/en/stable/api/pxssh.html

import pexpect 
import pxssh
import getpass

key_pub = "ssh-xxx xxx xxx@xxx.xxx.io"

try:
    s = pxssh.pxssh()

    # prompt for hostname, username and password
    hostname = raw_input('hostname: ')
    username = raw_input('username: ')
    password = getpass.getpass('password: ')
    s.login(hostname, username, password)

    # mkdir and chmod .ssh directory
    mkdir_dotssh_cmd = ( "mkdir /root/.ssh" )
    chmod_dotssh_cmd = ( "chmod 600 /root/.ssh" )
    s.sendline( mkdir_dotssh_cmd )
    s.sendline( chmod_dotssh_cmd )

    # create authorized_keys file with public key
    # chmod authorized_keys file
    create_authkey_cmd = ( "echo "+key_pub+" > /root/.ssh/authorized_keys" )
    chmod_authkey_cmd = ( "chmod 644 /root/.ssh/authorized_keys" )
    s.sendline( create_authkey_cmd )
    s.sendline( chmode_authkey_cmd )
    s.sendline( 'ls -ltrah /root/.ssh/authorized_keys' )
    print(s.before)
    s.prompt()
    s.sendline( 'cat /root/.ssh/authorized_keys' )
    print(s.before)
    s.prompt()
    print(s.before)
    s.logout()

except pxssh.ExceptionPxssh as e:
    print("pxssh failed on login.")
    print(e)

