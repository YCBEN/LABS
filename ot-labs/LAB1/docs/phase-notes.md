# Phase notes

## Phase 1

- Done: PLC and field simulator on Open vSwitch (VLAN 100 control, VLAN 90 field);
  OpenPLC runs the tank-level program; switch state saved in `configs/ovs-phase1.txt`.
- Skipped: a stand-alone packet-capture baseline. Capturing from GNS3 links hit file
  permission problems, and the baseline will be recorded by Malcolm in Phase 4.
- Incident write-up: see `troubleshooting.md`.

## Phase 2 (in progress)

- Part 1, step B done: OPNsense VM created in GNS3 (QEMU, 2 vCPU, 2 GB RAM, qcow2 disk,
  KVM acceleration, VNC console, 2 adapters) and installed to disk.
- Next: wire adapter 0 to the Open vSwitch trunk (eth0), management VLAN 99, VLAN
  interfaces 100, 200 and 210, then Part 2 (Level 2 containers and conduit rules).
- Credentials are kept out of the repository. The firewall configuration export is
  private because it contains password hashes.

## Phase 2, Part 1 (in progress)

- Done: OPNsense installed; trunk to Open vSwitch eth0; out-of-band management through a
  dedicated card (vtnet2, 10.250.99.1/24) with a verified ping.
- Design change: management no longer uses a VLAN on the switch (see ip-vlan-plan.md).
- Next: disable the placeholder WAN, create VLAN interfaces 100, 200 and 210, then Part 2.
- LAB1 stays strictly air-gapped; outbound-only access is left to a later lab.
