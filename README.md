# lenze_ethernet_ip

## Physical Setup

First controller: 
* 192.168.124.16
* connected to enp7s0 via ethernet 

Second controller: 
* 192.168.124.17
* connected to enp6s0 via ethernet

Network configuration:
Set routes using `ip route`-command so that the network-stack knows which network-device to use for each of the belt-controller:
* `ip route add 192.168.124.16 via 0.0.0.0 dev enp7s0`
* `ip route add 192.168.124.17 via 0.0.0.0 dev enp6s0`
