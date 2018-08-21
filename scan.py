#!/usr/bin/env python3
"""
scan a given network using the MAC broadcast address
syntax: ./scan.py -t 10.0.0.1/24

version 1.0 Aug 2018

"""

import scapy.all as scapy
import optparse


def get_arguments():
    # Get target IP address or range for scan
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target",
                      dest="target",
                      help="Target IP or range")
    (options, arguments) = parser.parse_args()
    return options


def scan(ip):
    # Use the broadcast to get available MAC addresses in the give range
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast,
                              verbose=False, timeout=1)[0]

    # Build a list IP/MAC associations found in the given range
    clients_list = []
    for element in answered_list:
        client_dict = {"IP": element[1].psrc,
                       "MAC": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list


def print_result(results_list):
    print("IP\t\t\tMAC Address\n-----------------------------------------")
    for client in results_list:
        print(client["IP"] + "\t\t" + client["MAC"])


options = get_arguments()
scan_result = scan(options.target)
print_result(scan_result)
