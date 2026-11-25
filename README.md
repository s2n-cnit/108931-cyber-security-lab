# Cyber Security Laboratories — MSc Internet Engineering

Four supervised sessions (12 hours), in English. Students observe network traffic, establish trust with TLS, enforce network segmentation, and evaluate intrusion detection. Original lab identifiers 01, 02, 03 and 05 are preserved.

| Session | Topic | Hours | Lab grade |
|---|---|---:|---:|
| [01](labs/lab01-traffic-analysis/README.md) | Network traffic analysis | 3 | 25% |
| [02](labs/lab02-tls-pki/README.md) | TLS and PKI | 3 | 25% |
| [03](labs/lab03-firewall/README.md) | Firewall and segmentation | 3 | 25% |
| [05](labs/lab05-intrusion-detection/README.md) | IDS and prevention concepts | 3 | 25% |

## Start here

1. Read the [syllabus](docs/syllabus.md), [safety policy](docs/safety.md) and [environment guide](environment/README.md).
2. Use an instructor-managed Ubuntu 24.04 VM, with 4 vCPU, 8 GB RAM and 40 GB disk recommended. Never run the network experiments on a production host.
3. Install dependencies and start the isolated topology following the environment guide. The bundled PCAPs can also be analyzed offline without Mininet.
4. Work through each lab and submit the artifacts described in its manual, using the [report template](docs/report-template.md).

## Repository layout

- `labs/`: student manuals, configuration templates, utilities and exercises.
- `environment/`: installation, virtual topology, local services and certificate generation.
- `datasets/`: deterministic synthetic PCAP files and labels; no real user data.
- `tools/`: dataset generator, experiment statistics and IDS metrics.
- `docs/`: syllabus, grading, reporting, references and optional practical exam (student brief).
- Instructor solutions are distributed separately. Test labels and generator are included for self-study; instructors should withhold them for blind assessment (see dataset guide).
- `tests/`: offline automated tests; `.github/workflows/`: CI for those tests.

## Some Considerations

- Offline Python utilities
- Dataset construction and certificate generation can be checked locally.
- Live Mininet, nftables, Zeek and Suricata exercises require a Linux VM with installed tools and instructor smoke testing.
- Synthetic data are educational fixtures, not evidence of real-world IDS accuracy.
- All activity is limited to this isolated, authorized environment.
