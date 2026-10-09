#!/usr/bin/env python3
"""Usage: python3 tools/roadmap.py N
Phases 0..N are Done, phase N+1 is In progress, the rest are Planned.
Rewrites docs/roadmap.svg and the status column of the README roadmap table."""
import re, sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent.parent
P = [("0","Foundation",["Host VM, GNS3,","Docker images,","VLAN plan"]),
("1","Level 0 / 1",["PLC + field sim","on Open vSwitch","VLANs 90 / 100"]),
("2","Firewall + L2",["OPNsense, HMI,","SCADA, EWS,","conduit rules"]),
("3","Level 3 services",["Historian,","patch repo,","NTP / syslog"]),
("4","Monitoring",["Malcolm on a","SPAN / mirror","port"]),
("5","Threat intel",["MISP feeds","IOCs and rules","into Malcolm"]),
("6","Air-gap",["Remove uplinks,","transfer station,","offline imports"]),
("7","Use cases",["Patch testing,","attack and","detect"]),
("8","Documentation",["Diagrams, rules,","baselines,","runbook"])]
C = {"Done":("#2e7d32","DONE"),"In progress":("#e08a00","IN PROGRESS"),"Planned":("#8a94a3","PLANNED")}
n = int(sys.argv[1]) if len(sys.argv) > 1 else 0
status = ["Done" if i <= n else "In progress" if i == n+1 else "Planned" for i in range(9)]
W,H,cw,g,x0,y0 = 1840,470,184,20,20,150
o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Arial, Helvetica, sans-serif">',
f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
'<text x="920" y="52" font-size="34" font-weight="700" fill="#0f1b2d" text-anchor="middle">OT Cyber Lab: build roadmap</text>',
'<text x="920" y="88" font-size="20" fill="#5a6675" text-anchor="middle">Bottom-up, one phase at a time, each phase verified before moving up the Purdue model</text>',
f'<line x1="{x0+cw/2}" y1="{y0-20}" x2="{x0+8*(cw+g)+cw/2}" y2="{y0-20}" stroke="#c5ccd6" stroke-width="4"/>']
for i,(num,t,d) in enumerate(P):
    x = x0+i*(cw+g); col,lab = C[status[i]]
    o.append(f'<circle cx="{x+cw/2}" cy="{y0-20}" r="9" fill="{col}"/>')
    o.append(f'<rect x="{x}" y="{y0}" width="{cw}" height="260" rx="14" fill="#f4f6f9" stroke="{col}" stroke-width="3"/>')
    o.append(f'<path d="M{x} {y0+14} a14 14 0 0 1 14 -14 h{cw-28} a14 14 0 0 1 14 14 v30 h-{cw} z" fill="{col}"/>')
    o.append(f'<text x="{x+cw/2}" y="{y0+32}" font-size="20" font-weight="700" fill="#ffffff" text-anchor="middle">PHASE {num}</text>')
    o.append(f'<text x="{x+cw/2}" y="{y0+85}" font-size="21" font-weight="700" fill="#0f1b2d" text-anchor="middle">{t}</text>')
    for k,l in enumerate(d):
        o.append(f'<text x="{x+cw/2}" y="{y0+125+28*k}" font-size="17" fill="#2b3544" text-anchor="middle">{l}</text>')
    o.append(f'<rect x="{x+22}" y="{y0+205}" width="{cw-44}" height="34" rx="17" fill="{col}"/>')
    o.append(f'<text x="{x+cw/2}" y="{y0+228}" font-size="15" font-weight="700" fill="#ffffff" text-anchor="middle">{lab}</text>')
o.append(f'<text x="20" y="{H-20}" font-size="16" fill="#5a6675">Zones: Level 0/1 (control) → Level 2 (supervisory) → Level 3 (operations and security) · Firewall: OPNsense · Monitoring: Malcolm · Threat intel: MISP</text></svg>')
(HERE/"docs").mkdir(exist_ok=True)
(HERE/"docs"/"roadmap.svg").write_text("\n".join(o), encoding="utf-8")
rd = HERE/"README.md"
if rd.exists():
    lines = rd.read_text(encoding="utf-8").split("\n")
    pat = re.compile(r'^\| ([0-8]) \| (.*) \| (Done|In progress|Planned) \|$')
    for j,l in enumerate(lines):
        m = pat.match(l)
        if m: lines[j] = f"| {m.group(1)} | {m.group(2)} | {status[int(m.group(1))]} |"
    rd.write_text("\n".join(lines), encoding="utf-8")
print("Roadmap updated:", ", ".join(f"{i}={s}" for i,s in enumerate(status)))
