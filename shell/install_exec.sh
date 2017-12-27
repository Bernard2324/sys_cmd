#!/bin/bash

"""
Author: Maurice Green
Purpose: BASH script for Downloading/Installing/Configuring zabbix-agent
"""
function checkVersion() {
	version=`awk '{split($0, version, " "); {print version[3]}}' /etc/redhat-release | cut -d "." -f1`
}

function checkForZabbix() {

	present=`find ./ -name 'zabbix*.rpm' -exec ls -l {} \;`

	if [[ $present ]]; then
		return true
	else
		return false
	fi
}

function clearConfig() {
	echo "Clearing Configurations If Found"
	if [[ -d "/etc/zabbix/" ]]; then
		echo "Deleting Current Zabbix Configuration Files"
		rm -rf "/etc/zabbix/"
	else
		echo "No Config Present"
	fi
}

function getRPM {

	checkVersion
	echo "Running Version", $version

	case $version in
		"5")
			echo -n "Retrieving Zabbix Agent Version %version"
			shift
			wget "http://repo.zabbix.com/zabbix/3.2/rhel/5/x86_64/zabbix-release-3.2-1.el5.noarch.rpm"
			;;

		"6")
			echo -n "Retrieving Zabbix Agent Version $version"
			shift
			wget "http://repo.zabbix.com/zabbix/3.2/rhel/6/x86_64/zabbix-release-3.2-1.el6.noarch.rpm"
			;;

		"7")
			
			echo -n "Retrieving Zabbix Agent Version $version"
			shift
			wget "http://repo.zabbix.com/zabbix/3.2/rhel/7/x86_64/zabbix-release-3.2-1.el7.noarch.rpm"
			;;
		*)
			;;
	esac


}

function iptablesSetup() {

	echo "Building IPTABLES Rules to Allow Connection With Server"
	iptables -I INPUT -p tcp --dport 10050 -s 1.1.1.1 -j ACCEPT
	iptables -I OUTPUT -p tcp --sport 10050 -d 1.1.1.1 -j ACCEPT
}

function configSetup() {
	echo "Preparing Zabbix Configuration!"
	sed -i 's/Server=127.0.0.1/#Server=127.0.0.1/g' /etc/zabbix/zabbix_agentd.conf
	sed -i '$ a Server=1.1.1.1' /etc/zabbix/zabbix_agentd.conf
	sed -i '$ a TLSConnect=psk' /etc/zabbix/zabbix_agentd.conf
	sed -i '$ a TLSAccept=psk' /etc/zabbix/zabbix_agentd.conf
	sed -i '$ a TLSPSKFile=/etc/zabbix/zabbix_agentd.psk' /etc/zabbix/zabbix_agentd.conf
	sed -i '$ a TLSPSKIdentity=PSK 056' /etc/zabbix/zabbix_agentd.conf

	hexval=`openssl rand -hex 32`
	if [[ -f "/etc/zabbix/zabbix_agentd.psk" ]]; then
		:
	else
		touch "/etc/zabbix/zabbix_agentd.psk"
	
	fi
	echo $hexval > "/etc/zabbix/zabbix_agentd.psk"
}

if ! [[ -d '/home/zabbix/' ]]; then

	echo "Creating Zabbix Home Directory"
	mkdir "/home/zabbix"
	cd "/home/zabbix"
	echo "You Are now in `pwd`"
	clearConfig
	getRPM
	echo "Adding RPM to Database and installing yum repo"
	tfile=`ls -l *rpm | awk '{print $9}'`
	rpm -Uvh $tfile
	yum --enablerepo=zabbix -y install zabbix-agent
else
	cd "/home/zabbix"
	# check is for the rpm ONLY not the binary for zabbix_agentd
	if [[ checkForZabbix ]]; then
		echo "Zabbix rpm installed Present.  Checking to see if it's installed!"
		if [[ `pidof zabbix_agentd` ]]; then
			echo "Zabbix Already Intalled and Running!"
			exit 0
		else
			echo "Attempting to Start"
			if [[ -x `which zabbix_agentd` ]] 2>/dev/null; then
				service zabbix-agent start
				if [[ `pidof zabbix_agentd` ]]; then
					echo "Now Running"
					exit 0
				else
					echo "Failed to Start installed Zabbix Service"
					exit 1
				fi
			else
				echo "Checking to see if it at least exists!"
				if [[ -f "/sbin/zabbix_agentd" || -f "/usr/sbin/zabbix_agentd" ]]; then
					# unlikely to happen but doesn't hurt to handle it
					echo "Changing binary to executable format"
					chmod +x "/sbin/zabbix_agentd" 2>/dev/null
					chmod +x "/usr/sbin/zabbix_agentd" 2>/dev/null
					service zabbix-agent start
					if [[ `pidof zabbix_agentd` ]]; then
						echo "Agent Configured and Running"
						exit 0
					else
						echo "Failed to start after modification"
						exit 1
					fi
				else
					echo "No binary file found.  Not even in executable mode"
					yum --enablerepo=zabbix -y remove zabbix-agent 2>/dev/null
					clearConfig
					tfile=`ls -l *rpm | awk '{print $9}'`
					rpm -Uvh $tfile
					echo "RPM Executed!"
					yum --enablerepo=zabbix -y install zabbix-agent
				fi
			fi
		fi
	else
		cd "/home/zabbix"
		echo "Downloading RPM File and Executing it"
		clearConfig
		getRPM
		tfile=`ls -l *rpm | awk '{print $9}'`
		rpm -Uvh $tfile
		yum --enablerepo=zabbix -y install zabbix-agent
	fi
fi

# At this point, lets stop agent and make config changes
service zabbix-agent stop
echo "Stopped Zabbix Agent"

configSetup

echo "Setup Complete!  I will now start Zabbix Service!"
service zabbix-agent start

iptablesSetup

if [[ `pidof zabbix_agentd` ]]; then
	exit 0
else
	echo "Service Not running after Installation and Configuration!"
	exit 1
fi
