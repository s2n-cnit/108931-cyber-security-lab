# Lab 01 — Network traffic analysis and protocol security

3 hours | 100 points | 25% of lab grade. Tools: Wireshark/TShark, tcpdump, Zeek, curl, dig, Python, Nginx. Start isolated topology per environment guide; offline PCAP fallback available. Objectives: capture/filter TCP/IP, reconstruct TCP/DNS/HTTP, compare HTTP/HTTPS visibility, summarize flows and distinguish evidence from suspicion.

| Activity | Minutes |
|---|---:|
| Setup and briefing | 15 |
| Capture and TCP/IP analysis | 35 |
| DNS and HTTP | 30 |
| HTTP vs HTTPS | 30 |
| Zeek flow analysis | 35 |
| Unknown PCAP | 25 |
| Discussion/submission | 10 |

## A. Capture
From Mininet CLI (stop capture before reading):
```text
r1 tcpdump -ni eth0 -w work/lab01.pcap &
ext dig @10.0.10.1 web.lab.test
ext curl --resolve web.lab.test:80:10.0.20.10 http://web.lab.test/
ext curl --resolve web.lab.test:443:10.0.20.10 --cacert work/lab-ca.crt https://web.lab.test/
r1 pkill -INT -x tcpdump
```
Open in Wireshark. Apply `tcp`, `udp`, `dns`, `http`, `tls`, `icmp`, `tcp.flags.syn == 1`. Identify addresses, ports, sequence/acknowledgement numbers, SYN/SYN-ACK/ACK, DNS query/response, HTTP method/status and timing. Use frame numbers as evidence. If live unavailable, open `datasets/pcap/lab01-baseline.pcap` for DNS/HTTP; TLS requires the live capture or instructor TLS fixture.

## B. Visibility
Compare live HTTP and HTTPS requests with identical service and path. Fill `visibility.csv`; distinguish encrypted payload and visible IPs, ports, timing, packet size and conditional SNI visibility. Do not assume encryption hides all metadata or that certificate messages are plaintext in TLS 1.3. Discuss correct server identity validation.

## C. Zeek
From VM shell:
```sh
mkdir -p work/zeek01
(cd work/zeek01 && zeek -r ../lab01.pcap)
```
Inspect `conn.log`, `dns.log`, `http.log`, `ssl.log` where generated. Use `zeek-cut` or your own parser for counts, bytes, duration, protocol distribution and destinations. Explain differences between packet counts and flow counts. Plot one distribution. For offline dataset substitute absolute path to baseline PCAP.

## D. Unknown capture
Analyze `datasets/pcap/lab01-investigation.pcap` without inspecting instructor solutions. Identify unusual repeated connections, resource requests and metadata. Distinguish indicators from confirmed malicious behavior. Propose a legitimate alternative explanation. Document frame numbers and confidence.

## Lecture-linked application security worksheet (within DNS/HTTP and discussion time)
Using the synthetic examples in [lecture worksheet](lecture-worksheet.md), identify DNSSEC record roles and interpret email authentication results. Allocate 10 minutes from the DNS/HTTP block and use the provided baseline capture if live setup is slow. Submit short answers as part of protocol interpretation; no additional points or contact time.

## Submission and rubric
PCAP and annotated sequences; completed visibility matrix; Zeek logs and summary/plot; unknown PCAP investigation; report (3 pages). Score: capture/filter 20; protocol interpretation 25; HTTP/HTTPS security comparison 20; flow/anomaly analysis 25; documentation 10. Discussion: what metadata remains visible? Does anomaly imply attack? How do flow and packet methods differ? What are passive monitoring limitations?
