#!/usr/bin/python
from jsonrpclib import Server
import json
import ssl

#CREDS
user = "admin"
passwd = "Arista"
ssl._create_default_https_context = ssl._create_unverified_context

#VARIABLES
certname = 'certname'
keyname = 'key'
duration = '3650' # In days
country = 'US'
state = 'CA'
locality = 'SantaClara'
org = 'Example'
ou = 'IT'

def main():
  for SwitchNumber in range(1, 11): # Runs against 192.168.255.1-10 in order
    ip = "192.168.255." + str(SwitchNumber)
    #SESSION SETUP FOR eAPI TO DEVICE
    url = "https://%s:%s@%s/command-api" % (user, passwd, ip)
    ss = Server(url)

    #CONNECT TO DEVICE
    try:
      fqdn = ''
      hostnamejson = ss.runCmds( 1, ['show hostname'])
      fqdn = hostnamejson[0]['fqdn']
      response = ss.runCmds( 1, [ 'enable', 'security pki key generate rsa 2048 '+keyname,
      'security pki certificate generate self-signed '+certname+' key '+keyname+' validity '+duration+
      ' parameters'+
      ' common-name '+fqdn+
      ' country '+country+
      ' state '+state+
      ' locality '+locality+
      ' organization '+org+
      ' organization-unit '+ou+
      ' subject-alternative-name dns '+fqdn ])
      response = ss.runCmds( 1, [ 'enable', 'configure', 'management security',
      'ssl profile https-secure', 'certificate certname key key' ])
      response = ss.runCmds( 1, [ 'enable', 'configure', 'management api http-commands',
      'protocol https ssl profile https-secure' ])
    except:
      if fqdn:
        print 'failure @ '+fqdn
      if not fqdn:
        print 'failure @ '+ip
      pass

if __name__ == "__main__":
  main()