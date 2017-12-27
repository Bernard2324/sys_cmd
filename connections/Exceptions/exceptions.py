#!/usr/bin/env python

"""
Author: Maurice Green
Purpose: Exception Handling

I'm not readlly sure if i'm doing this correctly, it's my first time.  I'll have to read up on it and adjust if/as needed.

"""
import paramiko

class ZabbixAPIException(Exception):
    def __init__(self):
        Exception.__init__(self, "Zabbix API Parameter Error")


class Authentication(paramiko.ssh_exception.AuthenticationException):
    """
    Exception raised by Authentication Failures
    """
    pass

class BadCredentials(Authentication):
    def __init__(self):
        print "Failed to Successfully Authentication, please pass correct credentials"
        self.user2 = raw_input("Please Enter Username: ")
        self.passwd2 = raw_input("Please Enter Password: ")
        try:
            from connections.connections import sshConn
            sshConn(self.host, port=22, username=self.user2, password=self.passwd2, timeout=20)
        except:
            raise RuntimeError("Bad Authentication Credentials Passed Twice\n")
