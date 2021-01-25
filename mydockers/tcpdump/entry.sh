#! /bin/bash

mkfifo /tcpdump/tcpdump-pipe
/usr/sbin/tcpdump -U -i any -w - port not 22 > /tcpdump/tcpdump-pipe
