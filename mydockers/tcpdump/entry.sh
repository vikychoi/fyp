#! /bin/bash

mkfifo /tcpdump/tcpdump-pipe
tcpdump -U -i any -w - port not 22 | tee -a /tcpdump/tcpdump-pipe
tail -f /dev/null
