#!/bin/sh

. /etc/rc.common
CheckForNetwork

while [ "${NETWORKUP}" != "-YES-" ]
do
    sleep 5
    NETWORKUP=
    CheckForNetwork
done

/Users/danielnichols/miniconda3/bin/python3 main.py --check
