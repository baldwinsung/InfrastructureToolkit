#!/bin/bash


if [ -z $1 ]; then
	echo "$0 <hostname or IP address> <tcp port>"
	exit 1
fi

if [ -z $2 ]; then
	echo "$0 $1 <tcp port>"
	exit 1
fi

HOSTNAME_OR_IP="${1}"
TCP_PORT="${2}"
TIMEOUT="2"
MAIL_TO="NAME@BLAH.COM"

nc -w ${TIMEOUT} -vz ${HOSTNAME_OR_IP} ${TCP_PORT} 2&> /dev/null

if [ $? != 0 ]; then
	echo "${HOSTNAME_OR_IP} port ${TCP_PORT} is not available."
	echo "${HOSTNAME_OR_IP} port ${TCP_PORT} is not available." | mail -s "ALERT ${HOSTNAME_OR_IP} ISSUE" ${MAIL_TO}
fi
