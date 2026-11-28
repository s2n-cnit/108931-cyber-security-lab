# Lab 04 — Network intrusion detection and prevention

3 hours | 100 points | 25% of lab grade. Tools: Suricata, Wireshark, jq, Python, Mininet, tcpdump. Objectives: deploy passive IDS, analyze EVE events, design harmless synthetic signatures, evaluate flow-level classification and combine prevention/detection. Inline IPS is optional instructor demonstration, not required.

| Activity | Minutes |
|---|---:|
| IDS/IPS introduction | 20 |
| Configuration | 25 |
| PCAP analysis | 30 |
| Rule development | 35 |
| Evaluation | 40 |
| Integration | 20 |
| Discussion/submission | 10 |

## A. Configuration
Use installed Suricata YAML with EVE JSON alerts enabled. Copy it for submission, set HOME_NET to include 10.0.20.0/24 (or use supplied explicit destination in starter). Verify installed version. Use `-S` to load only the provided local rules, making results independent of external feeds. From VM shell:
```sh
mkdir -p work/ids-cal
suricata -T -c /etc/suricata/suricata.yaml -S "$PWD/labs/lab04-intrusion-detection/baseline.rules"
suricata -c /etc/suricata/suricata.yaml -S "$PWD/labs/lab04-intrusion-detection/baseline.rules" -r datasets/pcap/ids-calibration.pcap -l work/ids-cal
jq 'select(.event_type=="alert")' work/ids-cal/eve.json | head -40
```
Use a fresh directory per run to prevent mixing logs. If installed file permissions require it, run Suricata in dedicated VM with sudo. Record timestamp, tuple, signature ID, category, severity and flow ID; correlate packets.

## B. Custom signature
Baseline matches `/lab4-test-marker` anywhere in normalized HTTP URI, including benign look-alikes. Complete `tuned-starter.rules` to match only the exact designated URI (SID 1000001). Test with calibration dataset, inspect false positives and false negatives. Use harmless HTTP requests only; no actual exploitation. Do not inspect held-out labels until rule tuning is complete. Preserve baseline and tuned rule hashes.

## C. Evaluation
Run each rule on separate directories and both calibration and held-out test PCAPs. Example for baseline held-out:
```sh
mkdir -p work/ids-test-base
suricata -c /etc/suricata/suricata.yaml -S "$PWD/labs/lab04-intrusion-detection/baseline.rules" -r datasets/pcap/ids-test.pcap -l work/ids-test-base
python3 tools/ids_metrics.py --labels datasets/labels/ids-test.csv --eve work/ids-test-base/eve.json --sid 1000001
```
Repeat with tuned rule. Join alerts by directional TCP tuple (one unique tuple per generated flow); multiple matching alerts count once. Report TP/TN/FP/FN, accuracy, precision, recall, FPR, F1. Undefined ratios N/A. Calibration and test sets differ in flow counts and source ports. Synthetic markers are labels, not genuine attacks. Discuss class imbalance, representativeness, generalization and data leakage. Optional real-world reading: https://www.unb.ca/cic/datasets/ids-2017.html (not bundled or needed).

## D. Integration
Use a dedicated test permission for HTTP from ext to web TCP 80, and capture on gateway eth1 (downstream of firewall). Compare firewall off + IDS, firewall on only, both enabled. For enabled IDS cases process captured PCAP offline; passive IDS does not block. Generate an ordinary HTTP request and the harmless marker using `ext curl http://10.0.20.10/lab4-test-marker`. For the firewall-on case add the explicit temporary permit before traffic, then remove it and repeat blocked request. Also test HTTPS with the same marker and valid CA; explain why encrypted URI is not visible to passive IDS. Compare permitted/blocked connections, alert counts, observed traffic and processing time; if available, Suricata stats for packet drops/CPU. Offline processing time is not inline latency. Discuss upstream vs downstream visibility and limits. Restore Lab 03 policy.

## Lecture-linked discussion (within existing integration/discussion time)
Classify the synthetic URI rule as a string signature. Contrast port and header-condition signatures conceptually. Explain which events a sensor outside the firewall, in the DMZ, or behind the internal firewall can observe. Correlate one alert with a firewall decision or explain why no corresponding event exists. Relate the evidence to incident management (collection, correlation, reporting). No live attack generation is required.

## Submission and rubric
Suricata YAML or relevant override, baseline/tuned rules, sanitized EVE logs, PCAP references, confusion matrices and plots, integrated comparison, report. Score: configuration 20; alert interpretation 15; custom rule 20; detection evaluation 25; integration 10; documentation 10. Discuss IDS vs IPS, limitations of signatures, encrypted traffic, segmentation, and potential ML extensions.
