#!/bin/bash

echo "dmesg_log"
file="log_dmesg.txt"
test=$(($1/30))

echo >>$file
echo >>$file
echo "test_nr: $test sample_nr: $1">>$file

echo >>$file
echo "***dmesg:">>$file

dmesg >>$file
dmesg -C

echo >>$file
echo "cat /proc/interrupts output:">>$file
cat /proc/interrupts >>$file
echo >>$file

#dmesg |tail -20 |grep -v axi>>$file
