# Phase notes

## Phase 1

- Done: PLC and field simulator on Open vSwitch (VLAN 100 control, VLAN 90 field);
  OpenPLC runs the tank-level program; switch state saved in `configs/ovs-phase1.txt`.
- Skipped: a stand-alone packet-capture baseline. Capturing from GNS3 links hit file
  permission problems, and the baseline will be recorded by Malcolm in Phase 4.
- Incident write-up: see `troubleshooting.md`.
