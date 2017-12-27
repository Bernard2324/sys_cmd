#!/usr/bin/env python

'''
Author: Maurice Green
Purpose: Auto Installtion of zabbix agent

'''
from connections.connections import sshConn
import SimpleHTTPServer
import SocketServer
import paramiko
import subprocess
import os, re
import threading
import socket
import sys

class install_mechs(sshConn):
	# we cannot use credentials.py - variable change
	def __init__(self, hostname, usr, pwd):
		super(install_mechs, self).__init__(hostname, usr, pwd)


	def execute(self, cmd):
		output_container = []
		(stdin, stdout, stderr) = self.conn.exec_command(cmd)

		for line in stdout.readlines():
			output_container.append(line)
		self.conn.close()
		return output_container

	def localServer(self):
		PORT = 8080
		Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
		httpd = SocketServer.TCPServer(
			("", PORT), Handler
		)
		print "Serving Connections at Port", PORT

		# only allow one connection
		httpd.handle_request()

	def getIP(self):

		data = subprocess.check_output(['ifconfig']).split()
		ints = [
			element for element in data if re.match(r'addr', element) is not None
		]
		ipaddr = ints[0].split(":")[1]
		return ipaddr

	def main(self):
		addr = self.getIP()
		command = "wget http://%s:8080/shell/install-exec.sh" % addr
		if self.conn is not None:
			print "Preparing Local Firewall Rules"
			subprocess.call('/shell/ipt_build.sh', shell=True)
			thread = threading.Thread(target=self.localServer)
			thread.daemon = True
			thread.start()
			print "Running Remote WGET Command"
			self.execute(command)
			subprocess.call('/shell/ipt_tear.sh', shell=True)
			print "Remotely Executing Zabbix Installation Script"
			run_script = "sh install-exec.sh"
			vals = self.execute(run_script)
			return vals
		else:
			return "No Established SSH Connection"
