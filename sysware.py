#!/usr/bin/env python
'''
Author: Maurice Green
Purpose: Main Script for argument handling/function calling
'''
from vmware.vmware_classes import vmware_mechs
from zabbix.install import install_mechs
from zabbix.zabbix_classes import zabb_mechs
import argparse
import sys
import re

def get_args():

    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--vmware',
        required=False,
        action='store',
        help="VM Guest Hosts for Querying", default=None
    )

    parser.add_argument('-z', '--zabbix',
        required=False,
        action='store_true',
        help="Run Against Zabbix for monitoring status"
    )

    parser.add_argument('-a', '--action',
        required=False,
        action='store',
        help="Zabbix Action"
    )

    parser.add_argument('-H', '--host',
        required=False,
        action='store',
        help='specify host name'
    )

    parser.add_argument('-l', '--list',
        required=False,
        action='store',
        help="list devices"
    )

    args = parser.parse_args()
    return args

def main():

    '''
    possible combinations:
    -vmware + 'names'                           // print vm hostnames
    -vmware + 'info' + host                     // print vm hostnames for specific list * can take regpattern
    -vmware + 'specs' + host                    // specifications for vm hosts *can take regpattern

    -zabbix + [action]'get' +  host             // get zabbix info for host
    -zabbix + [action]'create'                  // create zabbix host entry
    -zabbix + [action]'delete'                  // delete host entry
    -zabbix + [action]'install' + host          // install zabbix-agent on a particular host
    -zabbix + [action]'issues' [+host, +list]   // zabbix issue status for specific host or list of hosts *regex match
    '''
    args = get_args()
    def vmcaller(methcall, vm=None):
        vmw = vmware_mechs()
        call_funcs = {
            'names': vmw.allNames(),
            'info': vmw.basicInfo(vm),
            'specs': vmw.alloc_specs(vm),
            'specnames': vmw.specNames(vm)
        }
        results = call_funcs.get(methcall)
        return results

    def zabcaller(methcall, dev=None, config=None):
        zmc = zabb_mechs()
        call_funcs = {
            'get': zmc.gethost(dev),
            'create': zmc.createHost(config),
            'issues': zmc.issues(dev),
            'delete': zmc.deleteHost()
        }
        results = call_funcs.get(methcall)
        return results

    def zinstaller(host, user, passwd):
        zmi = install_mechs(host, user, passwd)
        results = zmi.main()
        return results

    if args.vmware is not None:
        if args.vmware == "names":
            res_container = vmcaller('names')
        elif args.vmware == "info":
            if not args.host:
                sys.exit("You Must Specify Host When requesting information [-H, --host]")
            res_container = vmcaller('info', vm=args.host)
        elif args.vmware == "specs":
            if not args.host:
                sys.exit("You Must Specify Host When requesting Information ")
            res_container = vmcaller('specs', vm=args.host)

    elif args.zabbix is not None:
        if args.action is None:
            sys.exit("You Must Specify A Zabbix Action: ['get', 'create', 'install', 'delete', 'issues']")
        elif args.action == "get":
            if not args.host:
                sys.exit("Please Specify Host")
            res_container = zabcaller('get', dev=args.host)

        elif args.action == 'create':
            hostParams = {
                'host': "",
                'groupid': "",
                'template': "",
                'dns': "",
                'ip': "",
            }
            for param in hostParams.keys():
                submit = raw_input ("Please Enter %s: " % param)
                hostParams[param] = submit
            res_container = zabcaller('create', config=hostParams)

        elif args.action == 'issues':
            if not args.host:
                if args.list is not None:
                    thosts = vmcaller('specnames', vm=args.list)
                else:
                    sys.exit("You Must Specify Host When requesting information [-H, --host]")
            else:
                thosts = args.host
            res_container = zabcaller('issues', dev=thosts)
        elif args.action == 'delete':
            res_container = zabcaller('delete')

        elif args.action == 'install':
            hst = raw_input("Enter Host: ")
            pwd = raw_input("Enter Password: ")
            usr = raw_input("Enter Username: ")
            res_container = zinstaller(hst, usr, pwd)

    return res_container

if __name__ == "__main__":
    data = main()
    print data