#!/usr/bin/env python

'''
Author: Maurice Green
Purpose: Classes for conneciton Establishment
'''
from pyVim.connect import SmartConnect, ConnectNoSSL, Connect, Disconnect
from credentials import zabbixCredentials, vmwareCredentials
from Exceptions.exceptions import BadCredentials
from libraryapi.zabapi import zbxapi
import pyVmomi
import requests
import getpass
import SimpleHTTPServer
import SocketServer
import subprocess
import paramiko
import threading
import socket
import ssl
import os
import re
import sys

class vmConn(vmwareCredentials):

	def __init__(self):
		super(vmConn, self).__init__()
		self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
		setattr(getattr(self, 'context'), 'verify_mode', 1)
		setattr(getattr(self, 'context'), 'check_hostname', True)
		self.context.load_default_certs()
		try:
			self.connection = SmartConnect(host=self.hostname, port=443, user=self.username, pwd=self.password)
		except ssl.SSLError:
			print "Attempting with SSL Context\n"
			self.connection = SmartConnect(host=self.hostname, port=443, user=self.username, pwd=self.password, sslContext=self.context)
		except:
			self.__repr__()

		self.datacenter = self.connection.content.rootFolder.childEntity[0]
		self.vmlist = [
			vm for vm in self.datacenter.vmFolder.childEntity
		]
	def __repr__(self):
		print "passwd=%s, hostname=%s, portnum=%s, username=%s" % (self.password, self.hostname, 443, self.username)

class zabconn(zabbixCredentials):

	def __init__(self):
		super(zabconn, self).__init__()
		# sub domain format for zabbix clean searching
		self.zabcleandomain = self.subdomain
		try:
			print "Attempinng Connection to Retrieve User Auth Token\n"
			self.zconn = zbxapi()
			self.zconn.login()
		except:
			print "Failed To Retrieve Authentication Token\n"


class sshConn(threading.Thread):

	def __init__(self, host, username, password):
		super(sshConn, self).__init__()
		self.conn = paramiko.SSHClient()
		self.user = username
		self.passwd = password

		if not re.match(r'(?!255)(?:\d+\.){3}(?!255)\d+', host):
			try:
				self.host = socket.gethostbyname(host)
			except:
				raise RuntimeError("Failed to Get IP Address Of Hostname")
		else:
			self.host = host

		self.conn.load_host_keys(filename=os.path.expanduser('~/.ssh/known_hosts'))
		self.conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		try:
			self.conn.connect(self.host, port=22, username=self.user, password=self.passwd, timeout=20)
		except BadCredentials:
			pass
