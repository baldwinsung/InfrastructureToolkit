#!/usr/bin/env python
#
# Script based off example on http://pexpect.readthedocs.io/en/stable/api/pxssh.html

from pexpect import pxssh
import pexpect 
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
    if username is 'root':
        mkdir_dotssh_cmd = ( "mkdir /root/.ssh" )
        chmod_dotssh_cmd = ( "chmod 700 /root/.ssh" )
    else:
        mkdir_dotssh_cmd = ( "mkdir /home/"+username+"/.ssh" )
        chmod_dotssh_cmd = ( "chmod 700 /home/"+username+"/.ssh" )

    s.sendline( mkdir_dotssh_cmd )
    s.sendline( chmod_dotssh_cmd )

    # create authorized_keys file with public key
    # chmod authorized_keys file
    if username is 'root':
        create_authkey_cmd = ( "echo "+key_pub+" > /root/.ssh/authorized_keys" )
        chmod_authkey_cmd = ( "chmod 644 /root/.ssh/authorized_keys" )
    else:
        create_authkey_cmd = ( "echo "+key_pub+" > /home/"+username+"/.ssh/authorized_keys" )
        chmod_authkey_cmd = ( "chmod 644 /home/"+username+"/.ssh/authorized_keys" )
    
    s.sendline( create_authkey_cmd )
    s.sendline( chmod_authkey_cmd )

    if username is 'root':
        s.sendline( 'ls -ltrah /root/.ssh/authorized_keys' )
    else:
        s.sendline( 'ls -ltrah /home/'+username+'/.ssh/authorized_keys' )

    print(s.before)
    s.prompt()

    if username is 'root' :
        s.sendline( 'cat /root/.ssh/authorized_keys' )
    else:
        s.sendline( 'cat /home/'+username+'/.ssh/authorized_keys' )

    print(s.before)
    s.prompt()
    print(s.before)
    s.logout()

except pxssh.ExceptionPxssh as e:
    print("pxssh failed on login.")
    print(e)

