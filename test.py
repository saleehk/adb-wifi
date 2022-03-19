#!/usr/bin/env python3

"""
Android11
Pair and connect devices for wireless debug on terminal

python-zeroconf: A pure python implementation of multicast DNS service discovery
https://github.com/jstasiak/python-zeroconf
"""

import subprocess
from zeroconf import ServiceBrowser, Zeroconf


TYPE = "_adb-tls-pairing._tcp.local."
NAME = "debug"
PASS = "123456"
FORMAT_QR = "WIFI:T:ADB;S:%s;P:%s;;"

CMD_SHOW = "qrencode -t UTF8 '%s'"
CMD_PAIR = "adb pair %s:%s %s"
CMD_DEVICES = "adb devices -l"

class MyListener:

    def remove_service(self, zeroconf, type, name):
        print("Service %s removed." % name)
        print("Press enter to exit...\n")

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        print("Service %s added." % name)
        print("service info: %s\n" % info)
        self.pair(info)

    def pair(self, info):
        cmd = CMD_PAIR % (info.server, info.port, PASS)
        print(cmd)
        subprocess.run(cmd, shell=True)


def main():
    text = FORMAT_QR % (NAME, PASS)
    subprocess.run(CMD_SHOW % text, shell=True)

    print("Scan QR code to pair new devices.")
    print("[Developer options]-[Wireless debugging]-[Pair device with QR code]")

    zeroconf = Zeroconf()
    listener = MyListener()
    browser = ServiceBrowser(zeroconf, TYPE, listener)

    try:
        input("Press enter to exit...\n\n")
    finally:
        zeroconf.close()
        subprocess.run(CMD_DEVICES, shell=True)


if __name__ == '__main__':
    main()
    