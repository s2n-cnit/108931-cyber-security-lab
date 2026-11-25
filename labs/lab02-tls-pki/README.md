# Lab 02 — TLS, PKI and secure communications

3 hours | 100 points | 25% of lab grade. Tools OpenSSL, Nginx, curl, Wireshark, Python. Objectives: create CA and server certificate, authenticate HTTPS, analyze handshake, diagnose validation failures, quantify overhead. Start with stopped topology for certificate regeneration; restart afterward.

| Activity | Minutes |
|---|---:|
| TLS/PKI introduction | 20 |
| Certificate generation | 35 |
| HTTPS setup | 30 |
| Handshake analysis | 30 |
| Validation experiments | 25 |
| Performance | 30 |
| Discussion/submission | 10 |

## A. PKI
Read `environment/make-certs.sh`. Reproduce the root/key/CSR/signing operations, explain CA constraints, SAN, key usage and EKU, and generate fresh local certificates in work/ (do not commit private keys). Inspect:
```sh
openssl x509 -in work/server.crt -text -noout
openssl verify -CAfile work/lab-ca.crt -verify_hostname web.lab.test work/server.crt
```
The script is a reference implementation; instructor may remove selected lines for assessed work. Explain the trust chain. Use only lab CA, do not install it in system trust store.

## B. Service
Inspect and adapt `environment/nginx.conf.template`; enable TLS 1.2/1.3, explain private key location. Launch topology and test via Mininet CLI:
```text
ext curl --resolve web.lab.test:443:10.0.20.10 --cacert work/lab-ca.crt https://web.lab.test/
```
## C. Handshake
Capture on r1 eth0 as Lab 01. Use exact TLS versions:
```text
ext curl --tlsv1.2 --tls-max 1.2 --cacert work/lab-ca.crt --resolve web.lab.test:443:10.0.20.10 https://web.lab.test/
ext curl --tlsv1.3 --tls-max 1.3 --cacert work/lab-ca.crt --resolve web.lab.test:443:10.0.20.10 https://web.lab.test/
```
Annotate ClientHello, ServerHello, observable certificate information and encrypted application data. TLS 1.3 encrypts handshake messages after ServerHello (excluding compatibility records); do not infer hidden contents from packet bytes. Explain confidentiality, integrity and authentication.

## D. Validation
Complete `validation.csv`. Test trusted CA (success), no lab trust (failure), wrong hostname (`wrong.lab.test` with --resolve), expired certificate (instructor fixture or offline `openssl verify -attime` beyond notAfter), unsupported TLS version (server rejects TLS 1.1; client may reject first, distinguish). Extended PKI missing intermediate is optional. Never bypass certificate verification as remediation.

## E. Performance
From Mininet CLI run the supplied measurement script inside ext:
```text
ext python3 labs/lab02-tls-pki/measure.py --output work/tls-times.csv --samples 30
```
From normal shell: `python3 tools/stats.py work/tls-times.csv --group mode --value total_ms`. Repeat for handshake_ms (HTTP not applicable). Compare mean/median/SD/95% CI, quantify relative overhead `(meanHTTPS-meanHTTP)/meanHTTP*100`. Each curl process establishes independent connection; no proxy, no session reuse; discuss VM scheduling and confidence interval assumptions. Plot results, not hypothetical values.

## Submission and rubric
Public CA/server certificates, Nginx config, annotated PCAP, validation matrix, raw timing/plots, report. Score: PKI 25; HTTPS 20; TLS analysis 20; validation 15; performance 10; reproducibility 10. Discuss trust anchor, hostname checks, metadata visibility and latency trade-offs.
