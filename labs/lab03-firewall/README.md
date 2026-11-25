# Lab 03 — Firewall configuration and network segmentation

3 hours | 100 points | 25% of lab grade. Tools: Mininet, nftables, tcpdump, curl, netcat, iperf3, Python. Objectives: design trust zones, implement stateful default-deny filtering, verify policy with positive and negative controls, measure overhead.

| Activity | Minutes |
|---|---:|
| Introduction | 15 |
| Topology setup | 35 |
| Policy design | 25 |
| Implementation | 40 |
| Verification | 30 |
| Performance | 25 |
| Discussion/submission | 10 |

## A. Architecture
Read `environment/topology.py`; draw four zones: external 10.0.10.0/24, DMZ 10.0.20.0/24, internal 10.0.30.0/24, management 10.0.40.0/24. Each host .10, gateway .1. Inspect `r1 ip addr` and `r1 ip route`. Explain why all inter-zone traffic traverses r1. Do not attach physical interfaces. Baseline: ensure each target TCP listener is actually reachable before enforcement.

## B. Policy
Allow new connections only: ext to web TCP 443; web to app TCP 8080; admin to web/app TCP 22. Return traffic for established connections allowed. All other forwarded traffic denied. Port 22 is a harmless TCP listener rather than actual SSH. Gateway-local input/output policies and production IPv6/anti-spoofing are outside scope. Fill `policy-tests.csv`.

## C. Implementation
Complete `firewall-starter.nft`; verify syntax and load only in r1 namespace via Mininet CLI:
```text
r1 nft -c -f labs/lab03-firewall/firewall-starter.nft
r1 nft -f labs/lab03-firewall/firewall-starter.nft
r1 nft list table inet lab_filter
```
If reloading, delete only the lab table first: `r1 nft delete table inet lab_filter`. Never flush host rules. Add per-rule counters, established/related acceptance and rate-limited logging. Explain order and state tracking.

## D. Verification
Use `nc -z -w 2 DEST PORT` from each listed source, record exit code using e.g. `ext sh -c 'nc -z -w 2 10.0.20.10 443; echo exit=$?'`. Test HTTPS via curl with lab CA as well. Verify actual counters; capture traffic if ambiguous. Record baseline and observed results, then compliance = correct/total x 100. Target 100%; investigate deviations. Ensure new connections for each test; no pre-existing sessions.

## E. Performance
Use a temporary iperf3 test permission: web already hosts iperf3 server on TCP 5201. Compare baseline (no lab_filter), stateful firewall with test rule, and same rule set with rate-limited logging of accepted test traffic. In CLI:
```text
r1 nft insert rule inet lab_filter forward iifname eth0 oifname eth1 ip saddr 10.0.10.10 ip daddr 10.0.20.10 tcp dport 5201 counter accept
ext iperf3 -c 10.0.20.10 -t 3 -J > work/throughput.json
```
For timing use repeated TCP connection measurements on an allowed port; for ping temporarily permit ICMP in all configurations and remove it afterward, or explicitly state RTT not measured. Run five throughput repetitions per configuration, using unique files. For logging variant insert a rate-limited log-only rule ahead of the test permit; do not alter permit semantics. Note stateful established rules may bypass logging depending on placement. Track CPU utilization and rule counters, optionally packet loss via controlled UDP test with separate explicit permissions. Degradation = (baseline - firewall)/baseline x 100. Remove temporary rules by handle (`nft -a list chain ...`; `nft delete rule ... handle N`) or reload original policy. Verify policy again. Discuss VM/CPU scheduling and logging limitations.

## Submission and rubric
Topology/script, policy matrix, nftables configuration, test evidence, raw measurements and plots, report. Score: topology/routing 20; policy design 15; firewall 25; validation 20; performance 10; documentation 10. Discuss stateful vs stateless, least privilege, positive/negative tests and performance trade-offs.
