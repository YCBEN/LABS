#!/bin/sh
# Run on the Open vSwitch console in GNS3.
ovs-vsctl set port eth1 tag=100   # PLC1 control NIC
ovs-vsctl set port eth2 tag=90    # PLC1 fieldbus NIC
ovs-vsctl set port eth3 tag=90    # field-sim
ovs-vsctl set port eth4 tag=100   # tap0 temporary workstation
ovs-vsctl show
