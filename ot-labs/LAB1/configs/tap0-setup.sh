#!/bin/sh
# Temporary workstation interface on the VM. Re-run after every reboot.
sudo ip tuntap add dev tap0 mode tap user "$USER"
sudo ip addr add 10.250.10.250/24 dev tap0
sudo ip link set tap0 up
