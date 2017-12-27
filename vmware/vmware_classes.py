#!/usr/bin/env python

'''
Author: Maurice Green
Purpose: Class Methods for VMWare actions
'''
from connections.connections import vmConn
from pyVim.connect import Disconnect
import pyVmomi
import re

class vmware_mechs(vmConn):

	def __init__(self):
		super(vmware_mechs, self).__init__()
		self.container_basic = self.vmlist
		check = re.compile(r'\s+((-)?(\s+)?)[a-zA-Z0-9]+')
		self.vmNames = [
			check.sub("", vm.name.lower()) for vm in self.container_basic
		]

	def allNames(self):
		# all hostnames in VMWare Vcenter
		return self.vmNames

	def specNames(self, name):
		# specific name information
		sizet = len(name)
		vm_reduced = [
			vm for vm in self.vmNames if vm[0:sizet] == 'name'
		]
		return vm_reduced

	def basicInfo(self, virtual_machine=None):
		# Just uuid, name, guest for the passed VM
		attributes = {
			'uuid': "",
			'name': "",
			'guest': "",
		}

		print "Searching Relevant Matches!"
		sizet = len(virtual_machine)
		vm_reduced = [
			vm for vm in self.vmNames if vm[0:sizet] == virtual_machine
		]
		for match in sorted(vm_reduced, reverse=True):
			position = self.vmNames.index(match)
			vmFocus = self.container_basic[position]
			attributes['uuid'] = vmFocus.config.uuid
			attributes['name'] = vmFocus.name
			attributes['guest'] = vmFocus.config.guestFullName
		return attributes


	def alloc_specs(self, virtual_machine):
		# Allocated Specifications for passed host: CPU/Cores per Socket/Memory
		specifications = {
			'CPU': "",
			'Memory': "",
			'CPU/socket': "",
			'guest': ""
		}
		sizet = len(virtual_machine)
		vm_reduced = [
			vm for vm in self.vmNames if vm[0:sizet] == virtual_machine
		]
		for match in sorted(vm_reduced, reverse=True):
			position = self.vmNames.index(match)
			vmFocus = self.container_basic[position]
			specifications['CPU'] = virtual_machine.config.hardware.numCPU
			specifications['Memory'] = virtual_machine.config.hardware.memoryMB
			specifications['CPU/socket'] = virtual_machine.config.hardware.numCoresPerSocket
			specifications['guest'] = vmFocus.config.guestFullName
		return specifications

	def close(self):
		Disconnect(self.connection)
