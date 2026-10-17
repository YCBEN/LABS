
## Management network (Phase 2 change)

Management is out-of-band: the VM's tap0 (10.250.99.250) is wired through the GNS3 Cloud
node straight to a dedicated OPNsense card (vtnet2, LAN 10.250.99.1/24). It does not use
the switch, so VLAN 99 is no longer carried on the trunk. The OPNsense WAN card is left
unplugged to keep the lab air-gapped.
