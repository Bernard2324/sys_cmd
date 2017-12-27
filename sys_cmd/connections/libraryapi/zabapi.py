#!/usr/bin/env python

'''

                                            ** Credit Notification **

    This script is HEAVILY Based off pyzabbix API, written by Lukecyca, he is given full credit for the functionality
    of the code in this script.  I do not want users of sysware_cmd to download the separate package modules, and I have also
    trimmed the code for sysware_cmd specific useage.  Although I have heavily modified it, he deserves much credit.

                                            ** Credit Notification **
'''

from __future__ import unicode_literals
from connections.credentials import zabbixCredentials
from connections.Exceptions.exceptions import ZabbixAPIException
import requests
import json

# ### I do not want logging ### #

class zbxapi(zabbixCredentials):

    def __init__(self, use_authenticate=False, timeout=None):
        super(zbxapi, self).__init__()
        self.session = requests.Session()
        self.session.verify = False
        try:
            self.session.headers.update({
                'Content-Type': 'application/json-rpc',
                'User-Agent': self.header,
                'Cache-Control': 'no-cache'
            })
        except:
            raise RuntimeError("Failed To Modify HTTP Headers")

        self.use_authenticate = use_authenticate
        self.auth = ''
        self.id = 0
        self.timeout = timeout

        # we already have self.url and self.urlapi from the zabbixCredentials class


    def login(self):

        if self.use_authenticate:
            raise ZabbixAPIException

        self.auth = self.user.login(user=self.username, password=self.password)

    def api_version(self):
        return self.apiinfo.version()

    def do_request(self, method, params=None):
        request_json = {
            'jsonrpc': '2.0',
            'method': method,
            'params': params or {},
            'id': self.id
        }

        if self.auth and method != 'apiinfo_version':
            request_json['auth'] = self.auth

        response = self.session.post(
            self.urlapi,
            data=json.dumps(request_json),
            timeout=self.timeout
        )
        response.raise_for_status()
        if not len(response.text):
            raise ZabbixAPIException

        try:
            response_json = json.loads(response.text)
        except ValueError:
            raise ZabbixAPIException

        self.id += 1
        if 'error' in response_json:
            if 'data' not in response_json['error']:
                response_json['error']['data'] = "No Data"
            msg = "Error {code}: {message}, {data}".format(
                code=response_json['error']['code'],
                message=response_json['error']['message'],
                data=response_json['error']['data']
            )
            raise ZabbixAPIException
        return response_json

    def __getattr__(self, attr):
        return zbxObjectClass(attr, self)


class zbxObjectClass(object):
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent

    def __getattr__(self, attr):
        def fn(*args, **kwargs):
            if args and kwargs:
                raise TypeError("Found Both Args and Kwargs")

            return self.parent.do_request(
                '{0}.{1}'.format(self.name, attr),
                args or kwargs
            )['result']
        return fn
