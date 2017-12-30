[![ld Status](https://travis-ci.org/Bernard2324/sys_cmd.svg?branch=master)](https://travis-ci.org/Bernard2324/sys_cmd)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[<a href="https://www.github.com/Bernard2324/sys_cmd" target="_blank">![sys_cmd](https://img.shields.io/pypi/v/nine.svg)]()
# Sys_cmd:   A Command line tool for Linux Admins 

This is a command line tool to help make my job as a Systems Engineer a little easier.  This happens to be my first actual 'project'
I normally write scripts and stop there.  I will be adding additional components such as SPLUNK, AWS, and various security features to
help with day-to-day tasks.  As I improve my Python and dicover more bugs/better ways of doing things, I will update the code.

# Dependencies

I used a number of publically available modules to build this script; these must be present for it to work properly.  I will also include SDK's in the list, that will be needed to support future realeases (*currently in development*):

Python Modules:
- PyVmomi
- PyVim

SDK's:
- [x] VMWare
- [ ] Boto3 (Amazon AWS)
- [ ] SPLUNK-SDK (SPLUNK)

+ All Others come natively installed with python 2.7+ (Must use 2.7 or above or replace all uses of subprocess.check_output, etc)

# Suported Environments:

This command line tool is for Linux! I have only tested on CentOS6/7, however, I'm confident it will work on just about any linux flavor; some obvious changes will be needed.  The install-exec.sh script uses a function for determining centos version and downloading the centos zabbix-client.  These will require modification if using a different distrubution.

the install action for zabbix cmd, only works if the target zabbix client is a Linux Device.  I may add functionality for Windows, however, it will be a while.

# Future Features:

Future features will include: AWS support, SPLUNK Support, configuration file for storing servernames, and extra config.  I do plan on adding controls for secure password storage; I certainly don't want to enter credentials everytime I use this tool, nor do I want them hardcoded.  

I will continue making efforts to make this tool a legitimate workplace solution, which will take some time.  By legitimate, I mean, my end goal to see this become a common use for Linux/DevOps Engineers.  This will be a gradual process, as I'm not a professional Developer.  For starters, you can expect the addition of a few features commonly seen, such as: setup.py, initial configuration assistance, usage examples, and multi-platform (Linux-only) support.  Like I said, I'm not a professional developer, and have lots to learn regarding Best Practices, especially when it comes to Application OOP.  I will also add more relevent methods for collecting more useful information.

This is a long term project, any contributions are welcome; please email me at bernard.infosystems@gmail.com.  You're more than welcome to contribute directly here as well!

