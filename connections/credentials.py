#!/usr/bin/env python

'''
Author: Maurice Green
Purpose: Username, Password, URL configurations

I realize many of you will not want to store passwords in plain text, feel free to 
modify code in a way that pleases you!

***
This FILE should be configured before running the tool.  As you can see, it will check for these values and only prompt for passwords
***
'''

from getpass import getpass

class zabbixCredentials(object):
	def __init__(self):
		self.url = 'https://zabbixserver.sub.domain.com'
		self.urlapi = self.urljoin('https://', 'sub.company.com', '/zabbix/api_jsonrpc.php')
		self.username = 'johndoe'
		self.password = getpass("Please Enter Zabbix User Password: ").strip() # get rid of that whitespace
		# I used the header because our server will not let random terminals connect :)
		self.header = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
		self.subdomain = 'sub.domain.com'
		
	def urljoin(self, *urlcomponents):
		# must be in format: protocol, [sub]domain.topleveldomain, uri
		# Ex: http://, sub.domain.com, /zabbix/api_jsonrcp.php
		return "".join(urlcomponents)

class vmwareCredentials(object):
	def __init__(self):
		self.hostname = 'vcenter.sub.domain.com'
		self.username = 'adminjohn'
		self.password = getpass("Please Enter VCenter Password: ").strip()

