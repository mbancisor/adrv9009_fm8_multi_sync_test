#!/bin/bash

cd /home/analog/git/adrv9009_fm8_multi_sync_test
sleep 15
sudo ./log.sh 127.0.0.1 10.48.65.98 |&tee -a output.txt

