#!/usr/bin/env python3
"""
change a local MAC address
syntax: ./change_mac.py -i eth0 -m 00:11:22:33:44:55
v1.1 Aug 2018
johnroge -> outlook.com

Last changes: created main(), adding documentation
"""

import re
import subprocess
import optparse


# TODO: save off current MAC address and give ability to roll back
def get_current_mac(interface):
    """
    Use regex to filter ifconfig for current MAC address
    :param interface: e.g. eth0
    :return: MAC address
    """
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w\:\w\w\:\w\w\:\w\w:\w\w:\w\w",
                                          ifconfig_result.decode("utf-8"))

    # return either a valid MAC address or an error statement
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


def main():
    # get user args, get current MAC address, change MAC, validate change
    options = get_arguments()

    current_mac = get_current_mac(options.interface)
    print("Current MAC = " + str(current_mac))

    change_mac(options.interface, options.new_mac)

    current_mac = get_current_mac(options.interface)
    if current_mac == options.new_mac:
        print("[+] MAC changed to " + current_mac)
    else:
        print("[-] ERROR: MAC address not changed")


if __name__ == '__main__':
    main()