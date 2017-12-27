#!/usr/bin/env python

from setuptools import setup

setup(
	name='sys_cmd',
	version='1.1.1',
	install_requires = [
		"requests>=1.0"
	],
	description="Command Line Tool For SysAdmins",
	author="Maurice Green",
	author_email="bernard.infosystems@gmail.com",
	license="MIT License: Copyright (c) 2017 Maurice Green",
	keywords="linux zabbix vmware python command-line-tool",
	url='http://github.com/Bernard2324/sysware_cmd',
	classifiers=[
		"Programming Language :: Python",
		"Programming Language :: Python :: 2.7",
		"License :: OSI Approved :: MIT",
		"Operating System :: Linux",
		"Development Status :: 1 - Beta",
		"Natural Language :: English",
		"Topic :: System :: Systems Administration"
	],
	packages=['sys_cmd', 'sys_cmd.connections', 'sys_cmd.vmware', 'sys_cmd.shell', 'sys_cmd.zabbix', 'sys_cmd.connections.libraryapi', 'sys_cmd.connections.Exceptions']
)

