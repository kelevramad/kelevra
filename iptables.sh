#!/bin/sh
clear
ifconfig at0 192.168.10.1 netmask 255.255.255.0
ifconfig at0 mtu 1400
echo 1 > /proc/sys/net/ipv4/ip_forward
iptables -t nat -A PREROUTNG -p udp -j DNAT -to 192.168.10.1
iptables -P FORWARD ACCEPT
iptables --apend FORWARD --in-interface at0 -j ACCEPT
iptables --table nat -append POSTROUTING --out-interface eth0 -j MASQUERADE
iptables -t nat -A PREROUTING -p tcp -destination-port 80 -j REDIRECT -to-port 10000
