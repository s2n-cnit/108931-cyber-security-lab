#!/usr/bin/env bash
set -euo pipefail
umask 077
out=${1:-work}
mkdir -p "$out"
openssl req -x509 -newkey rsa:2048 -nodes -days 365 -sha256 \
  -subj '/CN=Lab Root CA' -addext 'basicConstraints=critical,CA:TRUE' \
  -addext 'keyUsage=critical,keyCertSign,cRLSign' -keyout "$out/lab-ca.key" -out "$out/lab-ca.crt"
openssl req -new -newkey rsa:2048 -nodes -subj '/CN=web.lab.test' \
  -keyout "$out/server.key" -out "$out/server.csr"
cat > "$out/server.ext" <<'EXT'
basicConstraints=critical,CA:FALSE
keyUsage=critical,digitalSignature,keyEncipherment
extendedKeyUsage=serverAuth
subjectAltName=DNS:web.lab.test
EXT
openssl x509 -req -in "$out/server.csr" -CA "$out/lab-ca.crt" -CAkey "$out/lab-ca.key" -CAcreateserial -days 30 -sha256 -extfile "$out/server.ext" -out "$out/server.crt"
openssl verify -CAfile "$out/lab-ca.crt" -verify_hostname web.lab.test "$out/server.crt"
chmod 644 "$out/lab-ca.crt" "$out/server.crt"
