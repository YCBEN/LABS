# OT Labs

Hands-on labs for learning and testing **industrial control system (OT/ICS) cybersecurity**
in a safe, isolated, fully virtual environment. Each lab is self-contained: it has its own
README, documentation, and build files.

| Lab | Topic | Status |
|---|---|---|
| [LAB1](LAB1/) | Air-gapped Purdue-model lab with OPNsense, Malcolm and MISP | In progress |
| LAB2 | Same design rebuilt with a FortiGate firewall | Planned |

## Conventions

- One folder per lab (`LAB1`, `LAB2`, ...), each with its own `README.md` and `docs/`.
- Large files (ISOs, saved Docker images, packet captures) are **not** committed.
- Everything here is meant to run in an isolated lab. Never connect it to a production
  network.
