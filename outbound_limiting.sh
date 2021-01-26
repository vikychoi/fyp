#!/bin/sh

#check if is root
if [ `id -u` -ne 0 ]; then
   echo "This script requires root access."
   exit 1
fi

ELK_IP=23.99.106.134
packet_per_sec=1

# defining function
remap_tcp_port() {
    #this line route packet receive on port 22 to port 3000
    iptables -t nat -A PREROUTING -p tcp --dport 22 -j REDIRECT --to-ports 3000

    #this line route internal packet from port 22 to port 3000
    #iptables -t nat -A OUTPUT -p tcp -d localhost --dport 22 -j REDIRECT --to-ports 3000
}

# defining function
outbound_restrict() {
    #max $1 outbound packets per IP
    iptables -A OUTPUT -p tcp -d $ELK_IP -j ACCEPT
    iptables -A OUTPUT -p tcp --sport 22 -j ACCEPT
    ipatbles -A OUTPUT -p tcp --sport 50727 -j ACCEPT
    iptables -A OUTPUT -p tcp -m hashlimit --hashlimit-name outbound_limit --hashlimit-upto $1/sec --hashlimit-mode dstip -j ACCEPT
    iptables -A OUTPUT -p tcp -j DROP
}

# allowing port forwarding
#sysctl -w net.ipv4.ip_forward=1

# call the function and forward port 22 to 3000
#remap_tcp_port 

#flush all existing outbound rules
iptables -F OUTPUT

# restict outbound traffic, the parameter is the max outbound packets per IP
outbound_restrict $packet_per_sec
