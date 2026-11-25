#!/usr/bin/env bash
set -euo pipefail
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y mininet openvswitch-switch nftables tcpdump tshark wireshark nginx openssl curl dnsutils dnsmasq-base iperf3 suricata jq python3 python3-pandas python3-matplotlib netcat-openbsd
# Stop host-namespace services; lab instances are started explicitly.
sudo systemctl stop nginx suricata || true
printf 'Install Zeek separately if needed; record versions and snapshot VM.\n'
