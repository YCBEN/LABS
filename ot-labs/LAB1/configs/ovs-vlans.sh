#!/bin/sh
# Run on the Open vSwitch console in GNS3.
ovs-vsctl set port eth0 trunks=99,100,200,210   # trunk to OPNsense
ovs-vsctl set port eth1 tag=100                 # PLC1 control NIC
ovs-vsctl set port eth2 tag=90                  # PLC1 fieldbus NIC
ovs-vsctl set port eth3 tag=90                  # field-sim
ovs-vsctl set port eth4 tag=99                  # tap0 jump host (management)
ovs-vsctl show
