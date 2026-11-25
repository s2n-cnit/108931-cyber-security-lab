# Laboratory syllabus

**Degree:** MSc Internet Engineering | **Course:** Cyber Security | **Level:** Master's (EQF 7 indicative) | **Language:** English | **Contact hours:** 12 (4 x 180 minutes).

## Aims and prerequisites

Apply Internet engineering and experimental methodology to network security: observe, protect, prevent and detect. Prerequisites: TCP/IP, Linux CLI, basic Python and cryptography. Work individually or in pairs; each student must understand the submitted work.

## Learning outcomes

| ID | On completion students can | Primary labs |
|---|---|---|
| LO1 | Analyze traffic across TCP/IP layers | 01,05 |
| LO2 | Identify insecure protocol configurations | 01,02 |
| LO3 | Deploy authenticated encrypted communications | 02 |
| LO4 | Evaluate cryptographic guarantees and limitations | 02 |
| LO5 | Design segmentation and enforce access control | 03 |
| LO6 | Configure and evaluate network IDS | 05 |
| LO7 | Apply quantitative security and performance metrics | 02,03,05 |
| LO8 | Produce reproducible experiments and reports | all |
| LO9 | Discuss security/performance trade-offs | 02,03,05 |
| LO10 | Work ethically in authorized environments | all |

## Schedule

| Week | Session | Key output |
|---|---|---|
| 1 | 01 Traffic analysis | PCAP, protocol observations, flow summary |
| 2 | 02 TLS and PKI | Certificates, server config, validation and timing |
| 3 | 03 Firewall | Topology, policy matrix, test results and performance |
| 4 | 05 IDS | Rules, alerts, confusion matrix and integrated evaluation |

## Assessment

Each lab is 100 points and contributes 25% to the laboratory grade. Suggested course weighting: 30% lab and 70% theory examination, subject to institutional rules. See grading.md. Reports: maximum three pages each excluding references and supporting artifacts. Independent workload estimate: preparation 4 h, reports 8 h, analysis/revision 4 h; total including contact time 28 h. Optional 90-minute practical exam is outside the 12 hours.

## Pedagogical approach

A common isolated topology evolves from HTTP observation to HTTPS, default-deny firewall and passive IDS. Each session uses positive and negative controls, measurable evidence, and discussion of limitations. Instructor-prepared VM and datasets are necessary to keep the timings realistic. A passive IDS does not block traffic; inline IPS is an optional instructor demonstration.

## Research extensions

Encrypted flow classification, privacy-preserving telemetry, TLS/QUIC and post-quantum performance, intent-based network security, Zero Trust for edge and 5G/6G, explainable or federated intrusion detection and closed-loop security orchestration. These are optional research directions, not core assessed tasks.
