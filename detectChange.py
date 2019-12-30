#!/usr/bin/env /usr/local/bin/python3

import ipaddress
import netifaces
import datetime
import time

# TODO - test on windows (espectially link local)

previousAddress = ["INITIAL RUN"]
currentAddress = []
firstrun = True
lastchange = datetime.datetime.now()
while True:
    a = netifaces.ifaddresses('en0')
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
