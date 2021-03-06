#!/bin/bash


"""
Author: Maurice Green
Purspose: Teardown Firewall Rules
"""
echo "Invoking Local Server Instance"

function iptbuild() {
        echo "Building IP Tables Rules"
        shift
        iptables -I INPUT -p tcp --dport 8080 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT
        iptables -I OUTPUT -p tcp --sport 8080 -m state --state ESTABLISHED,RELATED -j ACCEPT
        echo "Done!  Rules in Place"
}

function iptteardown() {
        echo "Tearing Down IP Tables Rules"
        iptables -D INPUT 1
        iptables -D OUTPUT 1
}

if [[ -f "/home/jdoe/sysware_cmd/install-exec.sh" ]]; then
        echo "Tear Run"
        iptteardown
        echo "No more Connections Allowed At this point"
else
        echo "Installation BASH Script does not exist, serious problems!"

fi
