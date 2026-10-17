# Troubleshooting log

Real problems met while building LAB1, with the diagnosis and the fix.

## Incident 1: two copies of the lab running at once (Phase 1)

**Symptom.** The PLC level in OpenPLC was changing, but the packet capture on the
GNS3 link was empty and the Open vSwitch port counters did not increase.

**Diagnosis.**

| Check | Result | Meaning |
|---|---|---|
| `docker ps` | Two `field-sim` containers | A second copy of the lab was running |
| `ip route \| grep 10.250` | `10.250.10.0/24` listed twice (`br-l1` and `tap0`) | The VM had two paths to the same subnet |
| `docker ps -a` | Compose containers still present from the Phase 0 smoke test | The Docker Compose stack was never stopped |

**Root cause.** The Docker Compose smoke test (used to verify the images) and the GNS3
topology use the same addresses (`10.250.10.11` for the PLC, `10.250.1.21` for the
simulator). With both running, the browser and `ping` reached the compose PLC over the
Docker bridges, and that PLC polled its own simulator on its own bridge. The traffic never
crossed the GNS3 switch, so the switch counters stayed flat. The PLC looked healthy
because it was healthy, just the wrong one.

**Fix.**

1. `docker compose down`, then remove the leftover compose networks.
2. Confirm a single route to `10.250.10.0/24`, via `tap0` only.
3. Recreate the OpenPLC slave device and program on the GNS3 PLC, which starts empty.
4. Remove `restart: unless-stopped` from `docker-compose.yml` so the compose stack cannot
   come back on its own, and treat that file as an image build recipe only.
5. Add `configs/preflight.sh` to check for leftover compose containers and duplicate routes
   before each session.

**Lessons.**

- Two environments with identical addressing look fine from the outside. Always verify
  *which* instance you are talking to (container names, routes, counters).
- A flat counter is evidence, not noise: it showed the traffic was taking a different path.
- Separate the build tool (Compose) from the runtime (GNS3), and enforce it with a
  pre-flight check.

## Incident 2: container image builds failing on apt (Phase 0)

**Symptom.** `apt-get update` timed out inside `docker build`, while `pip` worked.

**Diagnosis.** The VM could fetch the Debian mirror over HTTP, but containers going through
Docker's NAT could not. HTTPS to the Debian CDN stalled at the TLS handshake, while GitHub
over HTTPS worked, which pointed to network filtering rather than a Docker problem.

**Fix.** Build with the VM's network (`network: host` in the compose build section).

## Incident 3: simulator register stuck at 0 (Phase 0)

**Symptom.** The Modbus server answered, but the tank level register read 0.

**Fix.** Rewrote the simulator: initial value at start-up, errors logged inside the update
loop, task reference kept, and exact register addressing.

## Incident 4: pings answered by the VM itself (Phase 2)

**Symptom.** Ping to 10.250.99.1 replied in 0.02 to 0.06 ms; the web interface would not open.

**Evidence.** `ip route get 10.250.99.1` said `local ... dev lo`; `ip -br addr` showed
`br-l0`, `br-l1` and `br-acc` holding 10.250.1.1, 10.250.10.1 and 10.250.99.1;
`docker ps -a` and `docker network ls` showed the otlab- containers and otlab_ networks;
`ip neigh` was empty (no ARP exchange).

**Root cause.** The VM is shut down at night and the compose lab was started again after
each boot. Each start recreates its bridges with the same addresses as the GNS3 lab, and
`br-acc` owned the firewall's address. A restart policy was ruled out (`restart=no`).

**Fix.** Removed the otlab- containers by name and the otlab_ networks (the GNS3. containers
were left alone). The compose file is now a build recipe only; `configs/start-lab.sh`
refuses to continue if stale compose containers or bridges exist.

**Lesson.** A reply under 0.1 ms is a warning: check which interface owns the address.

## Incident 5: tap0 lost its settings (Phase 2)

**Symptom.** The route to 10.250.99.1 pointed at ens33, or pings gave no reply and no error.

**Cause.** tap0 disappears when the VM restarts, and goes down and loses its address when
GNS3 stops the Cloud node.

**Fix.** Recreate it after the Cloud node is running (`configs/start-lab.sh`).

## Incident 6: Cloud node offered the internet card (Phase 2)

**Symptom.** The Cloud node's Ethernet tab listed ens33, br-l0 and br-l1.

**Meaning.** ens33 is the VM's internet-connected card and would break the air-gap.

**Fix.** Leave the Ethernet list empty; use only tap0 on the TAP tab. Switch counters then
showed eth4 idle because nothing was plugged into it, which led to the out-of-band
management design.

## Troubleshooting ladder

| Hop | Command | Good result |
|---|---|---|
| VM interface | `ip -br link show tap0` | UP, LOWER_UP |
| Route | `ip route get 10.250.99.1` | dev tap0 |
| ARP | `ip neigh show 10.250.99.1` | MAC, REACHABLE |
| Switch | `ovs-ofctl dump-ports br0` | counters rise |
| Firewall | `ifconfig vtnet2` (OPNsense shell) | status: active |
| Timing | ping reply time | above 0.1 ms |
