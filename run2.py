#!/usr/bin/env /usr/local/bin/python3

import ipaddress
import netifaces as ni
import datetime
from sys import exit
import time

# TODO - test on windows (espectially link local)
# TODO - improve first run behavior - time can be misleading on first cycle


def getInterface():
    """
    if an interface isn't provided on the command line, list all interfaces the OS knows about
    and prompt the user to select interface to monitor
    use index (not real interface name) as user input, because windows returns GUID, not friendly name
    :return: interface (string)
    """
    ifaces = ni.interfaces()
    print("List of interfaces by IP address (excludes interfaces with no v4 or MAC addresses")
    valid_interfaces = []
    for index, iface in enumerate(ifaces):
        try:
            ip = ni.ifaddresses(iface)[ni.AF_INET][0]["addr"]
            mac = ni.ifaddresses(iface)[ni.AF_LINK][0]["addr"]
            print("{}. IP: {} from Interface {} with MAC {}".format(index, ip, iface, mac))
            valid_interfaces.append(index)
        except:
            pass
    print("\n")
    valid_choice = False
    while not valid_choice:
        choice = int(input("Which interface to monitor? "))
        if choice in valid_interfaces:
            selected_if = ifaces[int(choice)]
            print("\nOK.  Monitoring {}".format(selected_if))
            valid_choice = True
        else:
            print("Invalid Interface selected (either doesn't exist or doesn't have a v4 addr. Try again")
    return selected_if


def monitorAddress(selected_interface):
    previousAddress = ["INITIAL RUN"]
    currentAddress = []
    firstrun = True
    lastchange = datetime.datetime.now()
    while True:
        a = ni.ifaddresses(selected_interface)
        now = datetime.datetime.now()
        if 30 in a.keys():        # check to see if the interface  has an IPv6 address (30 = AF inet6 )
            addresses = a[30]
            currentAddress = []
            for address in addresses:
                try:
                    ipaddress.ip_address(address['addr'])
                    currentAddress.append(address['addr'])
                except ValueError:
                    # if it isn't a valid IP address, it's likely link local
                    # on MAC, the link local is returned looking like
                    # fe80::811:8e07:48ef:d31%en0, which doesn't pass validation
                    if len(address) == 1:
                        print("only has link local addr")
                    pass
        else:
            print("no v6 address present on interface")
        # sort the lists to make them easier to read
        previousAddress.sort()
        currentAddress.sort()
        if firstrun:
            print("Script initializing at {} with the following addresses: \n{}".format(now, currentAddress))
            firstrun = False
        elif set(previousAddress) != set(currentAddress):
            print("\n!! address change detected between {} and {}".format(then, now))
            print("WAS: {}".format(previousAddress))
            print("NOW: {}".format(currentAddress))
            print("approximate time between change: {}".format(now - lastchange))
            lastchange = datetime.datetime.now()
        previousAddress = currentAddress
        then = now
        time.sleep(1)


def main():
    interface = getInterface()
    monitorAddress(interface)


main()
