import re
import smtplib
import dns.resolver
import argparse

#argparse
parser = argparse.ArgumentParser(description="Check to see if email address is legitimate")
parser.add_argument('-e','--email', help='Email to check',required=True,default=False)
args = parser.parse_args()

# Address used for SMTP MAIL FROM command  
fromAddress = 'corn@bt.com'

# Simple Regex for syntax checking
regex = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

# Email address to verify
addressToVerify = str(args.email)

# Syntax check
match = re.match(regex, addressToVerify)
if match == None:
	print('[-] %s does not appear to be formatted correctly.') % addressToVerify
	raise ValueError('Bad Syntax')

# Get domain for DNS lookup
splitAddress = addressToVerify.split('@')
domain = str(splitAddress[1])

# MX record lookup
records = dns.resolver.query(domain, 'MX')
mxRecord = records[0].exchange
mxRecord = str(mxRecord)

# SMTP lib setup (use debug level for full output)
server = smtplib.SMTP()
server.set_debuglevel(0)

# SMTP Conversation
server.connect(mxRecord)
server.helo(server.local_hostname) ### server.local_hostname(Get local server hostname)
server.mail(fromAddress)
code, message = server.rcpt(str(addressToVerify))
server.quit()

# Assume SMTP response 250 is success
if code == 250:
	print('[+] %s has valid formatting and is an active email address') % addressToVerify
else:
	print('[-] % has valid formatting but is not an active email address') % addressToVerify
