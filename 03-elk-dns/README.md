# 104781-cyber-security

Source code for exercise of Cyber Security Course (104781).

## DNS Tunneling with ELK

A machine learning job detected unusually large numbers of DNS queries for a single top-level DNS domain, which is often used for DNS tunneling.
DNS tunneling can be used for command-and-control, persistence, or data exfiltration activity.
For example, dnscat tends to generate many DNS questions for a top-level domain as it uses the DNS protocol to tunnel data.

## Prerequisites

1. **Install docker** from https://www.docker.com/products/docker-desktop.
2. **Install git** from https://git-scm.com/downloads.

## Install ELK with Docker

- Follow the README of this repository: <https://github.com/deviantony/docker-elk>.

## Setup ELK

- Configure ELK for DNS Tunneling: <https://www.elastic.co/guide/en/security/current/dns-tunneling.html>.
