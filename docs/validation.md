# Package validation

Performed during package creation: seven offline Python unit tests passed (metrics, undefined ratios, descriptive statistics, IP/TCP checksums, PCAP record counts, label counts, deterministic regeneration); Python source compilation and shell syntax checks passed. OpenSSL generated a fresh CA and leaf certificate and verified both trust and hostname successfully. Generated private keys were kept outside the repository.

Not performed: live Mininet topology execution, Nginx in namespace, firewall enforcement, Zeek analysis or Suricata rule execution. These require a configured lab VM. Instructor must run the environment smoke test before teaching. No real performance or detection measurements are included; expected values are synthetic fixture predictions.
