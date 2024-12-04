# Building a "Mini" Cyber Security Lab - SOC (IDS/IPS, SIEM, and Firewall)

Cyber Security is an umbrella term that comprises of different subcategories of a subcategory.

This lab setup is going to focus on the technical side for both the offensive and defensive side of Cyber Security where you are going to build a virtualized SOC (Security Operating Center) environment through VMware to detect the attacks that you are a going to simulate from a Kali machine.

VMware is a virtualization software where you could deploy and manage these virtual machines, think of it as like building a computer inside a computer.

![SOC Lab — Diagram](soc_lag-diagram.png)

## What you’ll need

- [VMware Workstation](https://www.vmware.com/products/desktop-hypervisor/workstation-and-fusion)
- [PFsense Firewall](https://www.pfsense.org/download)
- [Security Onion IDS/IPS and SIEM](https://github.com/Security-Onion-Solutions/security-onion/blob/master/Verify_ISO.md)
- [Kali Linux](https://www.kali.org/downloads)
- [Metasploitable 2](https://sourceforge.net/projects/metasploitable)

## Installation and configuration

Installing VMware is a straightforward process so lets go ahead and proceed with the firewall.

Here’s the PFsense firewall settings you can have. Ensure you have this networking settings to avoid errors. CPU, RAM and Hard Disk settings will vary depending on your system capacity.

![PFsense Configuration](pf_sense-config.png)

Once you’ve successfully installed PFsense, you will land on this interface where to setup the network interfaces and IP ranges for the machines.

![PFsense setup interfaces](pf_sense-setup_iface.png)

Select option 1 and assign these interfaces to your network cards.

![PFsense assignment interfaces](pf_sense-assign_iface.png)

Now that the network interfaces are set, lets assign the IP range for these interfaces.

![PFSense assignment IPs](pf_sense-assign_ip.png)

![PFsense set IP address options](pf_sense-set_ip_opts.png)

![PFsense enable DHCP Server for Attacker Interface (1)](pf_sense-enable_dhcp_attack_iface-1.png)

![PFsense enable DHCP Server for Attacker Interface (2)](pf_sense-enable_dhcp_attack_iface-2.png)

![PFsense enable DHCP Server for Victim Interface](pf_sense-enable_dhcp_victim_iface.png)

Now that the firewall is good to go, lets proceed with Security Onion which will be your IDS (Intrusion Detection System) and SIEM (Security Information and Event Management).

![Security Onion Configuration](sec_onion_config.png)

Once you’ve powered on Security Onion, follow these steps to install the security applications (Kibana, Zeek, Snort, Suricata, Elasticsearch and much more).

![Security Onion Installation (1)](sec_onion_install-1.png)
![Security Onion Installation (2)](sec_onion_install-2.png)
![Security Onion Installation (3)](sec_onion_install-3.png)

![Security Onion Setup](sec_onion_setup.png)

![Security Onion Setup Completed](sec_onion_completed.png)

Now that our IDS and SIEM is up, lets setup your Kali (attacker) machine.

![Kali Configuration](kali-config.png)

![Kali Config Interfaces](kali-iface.png)

Now that your Kali machine is all set and ready, lets setup your vulnerable target machine where you will simulate and practice attacks on.

You will be using Metasploitable 2 as target machine. Metasploitable 2 is a Linux box that is built for conducting penetration testing techniques for cyber security professionals. Installing Metasploitable 2 is a straightforward process, just power it on and you’re target is ready

![Metasploitable 2 Configuration](metasploitable_2-config.png)

![msfadmin :: msfadmin](msfadmin-msfadmin.png)

![msfadmin Ping](msfadmin-ping.png)

Alright, now that your environment is set up, lets try to simulate a simple FTP backdoor exploit and see if your IDS picks it up.

## Attack simulation

![alt text](attack_simulation-1.png)

![alt text](attack_simulation-2.png)

![alt text](attack_simulation-3.png)

![alt text](attack_simulation-4.png)

![alt text](attack_simulation-5.png)

As a SOC Analyst, what’s the first thing you would do if you see these kinds of logs in your SIEM? Re-image or segment that compromised machine then create a firewall rule to block that source IP and call it a day?
