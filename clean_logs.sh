#!/bin/bash
slave_IP=$1

read -p "!!!are you sure you want to delete all log files???"

echo "removing master data"
rm nr_runs.txt log.csv log_dmesg.txt log_jesd.txt log_dmesg_slave.txt log_jesd_slave.txt output.txt 
rm -rf ./test/*/
rm ./test/*.csv


if [ -n "$1" ]
then	
	echo "deleting slave data"
	sshpass -p 'analog' ssh -o StrictHostKeyChecking=no $slave_IP rm log_dmesg.txt log_jesd.txt 
fi

