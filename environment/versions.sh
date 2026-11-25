#!/usr/bin/env bash
uname -a
for x in python3 tshark zeek openssl nginx mn nft suricata iperf3; do
  command -v "$x" >/dev/null && { echo "--- $x"; "$x" --version 2>&1 | head -4; } || true
done
