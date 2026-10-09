#!/bin/sh
echo "== compose leftovers (should print nothing) =="
docker ps --format '{{.Names}}' | grep -E '^otlab-'
echo "== routes (expect only tap0 for 10.250.10.0/24) =="
ip route | grep 10.250
echo "== tap0 =="
ip addr show tap0 2>/dev/null | grep inet || echo "tap0 missing"
