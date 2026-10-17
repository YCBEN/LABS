#!/bin/sh
# Run after boot, and again after (re)starting the Cloud node in GNS3.
if docker ps -a --format '{{.Names}}' | grep -q '^otlab-'; then
  echo "STOP: compose lab containers exist (otlab-*). Remove them by name."; exit 1; fi
if ip -br link | grep -qE '^br-(l0|l1|acc)'; then
  echo "STOP: stale compose bridges present (br-l0, br-l1 or br-acc)."; exit 1; fi
ip link show tap0 >/dev/null 2>&1 || sudo ip tuntap add dev tap0 mode tap user "$USER"
sudo ip link set tap0 up
ip -4 addr show tap0 | grep -q 10.250.99.250 || sudo ip addr add 10.250.99.250/24 dev tap0
ip -br addr show tap0
ip route get 10.250.99.1 | head -1
