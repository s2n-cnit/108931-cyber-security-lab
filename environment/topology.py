#!/usr/bin/env python3
"""Isolated Mininet topology. Run from repo root inside dedicated VM."""
from pathlib import Path
import os, sys
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel

def main():
    root = Path.cwd().resolve()
    work = root / 'work'
    if os.geteuid() != 0 or not (work/'server.crt').exists():
        sys.exit('Run as root in lab VM, from repo root after make-certs.sh')
    if any(ch.isspace() for ch in str(root)):
        sys.exit('Use a repository path without spaces')
    setLogLevel('info')
    net = Mininet(controller=None, build=False)
    procs = []
    try:
        r = net.addHost('r1', ip=None)
        hosts = {}
        for i, (name, octet) in enumerate(zip(('ext','web','app','admin'), (10,20,30,40))):
            h = net.addHost(name, ip=f'10.0.{octet}.10/24', defaultRoute=f'via 10.0.{octet}.1')
            net.addLink(r,h,intfName1=f'eth{i}',intfName2='eth0')
            hosts[name] = h
        net.build(); net.start()
        for i, octet in enumerate((10,20,30,40)):
            r.cmd(f'ip addr add 10.0.{octet}.1/24 dev eth{i}')
        r.cmd('sysctl -w net.ipv4.ip_forward=1')
        conf = (root/'environment/nginx.conf.template').read_text().replace('@WORK@',str(work))
        (work/'nginx.conf').write_text(conf)
        procs.append(hosts['web'].popen(['nginx','-c',str(work/'nginx.conf'),'-g','daemon off;']))
        procs.append(r.popen(['dnsmasq','--no-daemon','--no-resolv','--no-hosts','--bind-interfaces','--interface=eth0','--interface=eth1','--interface=eth2','--interface=eth3','--address=/web.lab.test/10.0.20.10','--port=53']))
        for name, port in [('web',22),('app',22),('app',8080),('admin',22)]:
            procs.append(hosts[name].popen([sys.executable,str(root/'environment/tcp_service.py'),str(port)]))
        procs.append(hosts['web'].popen(['iperf3','-s']))
        print('Isolated topology started. Use ext/web/app/admin/r1 CLI prefixes.')
        CLI(net)
    finally:
        for p in procs:
            if p.poll() is None:
                p.terminate()
                try: p.wait(timeout=3)
                except Exception: p.kill(); p.wait()
        net.stop()
if __name__ == '__main__': main()
