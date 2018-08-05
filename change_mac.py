#!/usr/bin/env python3
"""
change a local MAC address
"""

import re
import subprocess
import optparse


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w\:\w\w\:\w\w\:\w\w:\w\w:\w\w",
                                          ifconfig_result.decode("utf-8"))

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] unable to read MAC address")


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface",
                      dest="interface",
                      help="Interface"
                           " to change MAC address")
    parser.add_option("-m", "--mac",
                      dest="new_mac",
                      help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] please specify an interface")
    elif not options.new_mac:
        parser.error("[-] please specify a new mac address")
    return options


def change_mac(interface, new_mac):
    print("[+] Changing " + interface + " MAC address to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])
    subprocess.call(["ifconfig", interface])


options = get_arguments()

current_mac = get_current_mac(options.interface)
print("Current MAC = " + str(current_mac))

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC changed to " + current_mac)
else:
    print("[-] ERROR: MAC address not changed")
