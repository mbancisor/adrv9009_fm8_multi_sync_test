#!/bin/bash
master_IP=$1
slave_IP=$2
slave="ip:${slave_IP}" 

pwd
cd /home/analog/git/adrv9009_fm8_multi_sync_test
pwd
acq_per_run=3

if [ -f "nr_runs.txt" ]; then
    prev_runs=$(cat nr_runs.txt)
    echo "continuing $prev_runs"
else 
    echo "new test"
    prev_runs=1
fi
#export PYTHONPATH=$PYTHONPATH:/usr/lib/python2.7/site-packages
total_runs=$prev_runs
for i in {1..3}
do

	echo "run $((total_runs)) times"
	echo "$(((total_runs)*acq_per_run)) samples"

	cd test
	sudo python3 ./adrv9009_som_multi_new.py "ip:localhost" $slave $total_runs
        cd ..

	wait
	./jesd_status.sh $(((total_runs)*acq_per_run))
	sudo sshpass -p 'analog' ssh -o StrictHostKeyChecking=no root@$slave_IP 'bash -s' < ./jesd_status.sh $(((total_runs)*acq_per_run))
	sudo sshpass -p 'analog' scp -o StrictHostKeyChecking=no root@$slave_IP:log_jesd.txt ./log_jesd_slave.txt 
	wait
	./dmesg_status.sh $(((total_runs)*acq_per_run))
	sudo sshpass -p 'analog' ssh -o StrictHostKeyChecking=no root@$slave_IP 'bash -s' < ./dmesg_status.sh $(((total_runs)*acq_per_run))
	sudo sshpass -p 'analog' scp -o StrictHostKeyChecking=no root@$slave_IP:log_dmesg.txt ./log_dmesg_slave.txt 
	wait

	total_runs=$((i+prev_runs))
	echo $total_runs>nr_runs.txt
done

sudo sshpass -p 'analog' ssh -o StrictHostKeyChecking=no root@$slave_IP poweroff
wait
python3 PDU.py 10.48.65.121 1 delayedReboot
python3 PDU.py 10.48.65.121 2 delayedReboot
python3 PDU.py 10.48.65.121 3 delayedReboot
poweroff
#reboot
