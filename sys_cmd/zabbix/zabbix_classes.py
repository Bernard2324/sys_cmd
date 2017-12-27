#!/usr/bin/env python
'''
Author: Maurice Green
Purpose: Class methods for zabbix actions
'''


from connections.connections import zabconn
import pyzabbix
import sys
import re

class zabb_mechs(zabconn):
	def __init__(self):
		super(zabb_mechs, self).__init__()

	def issues(self, hosts=[]):
		domain = re.compile(self.zabcleandomain)
		issue_params = {
			'only_true': 1, 'skipDependent': 1, 'monitored': 1,
			'active': 1, 'output': 'extend', 'expandDescription': 1,
			'expandData': 1, 'host': ""
		}
		setattr(self, 'hosts', hosts)
		for host in self.hosts:
			if not domain.match(host):
				host = host + "."+self.zabcleandomain
			issue_params['host'] = host
			issue_data = self.zconn.trigger.get(issue_params)
		devices_checked = {}
		devices_checked.setdefault(host, []).append([
			trigger['description'] for trigger in issue_data
		])
		return devices_checked

	def exists(self, obj):
		if isinstance(obj, pyzabbix.host):
			return all([self.zconn.host.isreadable({'host': obj})])
		elif isinstance(obj, pyzabbix.group):
			return all([self.zconn.hostgroup.isreadable({'name': obj})])
		elif isinstance(obj, pyzabbix.template):
			return all([self.zconn.template.isreadable({'host': obj})])
		else:
			raise AttributeError("You Did Not provide a valid Zabbix API Object\n")

	def createHost(self, configProposal):
		if not isinstance(configProposal, (dict, list)):
			raise TypeError("Invalid Configuration Proposal.  Must be Dictionary")

		if any(map(self.exists, [configProposal['host'], configProposal['groupid'],
			configProposal['template']])):

			raise TypeError("Invalid Zabbix API Object!\n")

		print "Attempting To Create Host[%s]" % configProposal['host']
		tempdata = self.zconn.template.get(name="")
		groupdata = self.zconn.hostgroup.get(name="")
		tgroupid = [
			dev['groupid'] for dev in groupdata if dev['name'] == configProposal['groupid']
		][0]

		ttempid = [
			dev['templateid'] for dev in tempdata if dev['name'] == configProposal['template']
		][0]

		create_host = self.zconn.host.create({
			"host": configProposal['host'],
			"groups": [{
				"groupid": tgroupid
			}],
			"templates": [{
				"templateid": ttempid
			}],
			"interfaces": [{
				"type": 1, "main": 1, "useip": 1, "ip": configProposal['ip'],
				"dns": configProposal['dns'], "port": "10050"
			}]
		})
		return create_host['hostids']

	def gethost(self, hosts):

		'''
		should be an array, even if only 1
		I'm returning all information for targeted hosts, so that the specific caller can
		determine which bits of information are desired from them
		'''
		hostdata = self.zconn.host.get(name="")
		hostinformation = [host for host in hostdata if host['name'] in hosts]
		return hostinformation

	def deleteHost(self):
		messages = []
		# hostnames will be a list of hosts to delete
		host_deletion = []
		while True:
			proceed = raw_input("Enter Host Name(press n to Stop): ")
			if not proceed[0].lower() == 'n':
				host_deletion.append(proceed)
			else:
				break
		# get the hostid's of all devices
		del_host_ids = [int(host['hostid']) for host in self.gethost(host_deletion)]
		print "Deleting Hosts: %s" % del_host_ids
		for hostid in del_host_ids:
			position = del_host_ids.index(hostid)
			message = self.zconn.host.delete(del_host_ids[position])
			messages.append(message)
		return messages
