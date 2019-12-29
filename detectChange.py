import netifaces
from time import sleep

# TODO - test on windows (espectially link local)
# TODO - alert on change, record time

while True:
    a = netifaces.ifaddresses('en0')
    if 30 in a.keys():        # check to see if the interface  has an IPv6 address (30 = AF inet6 )
        addresses = a[30]
        for address in addresses:
            try:
                ipaddress.ip_address(address['addr'])
                print(address['addr'])
            except ValueError:
                # if it isn't a valid IP address, it's likely link local
                # on MAC, the link local is returned looking like
                # fe80::811:8e07:48ef:d31%en0, which doesn't pass validation
                print("only has link local addr")
                pass
    else:
        print("no v6 address present on interface")
    sleep(5)
