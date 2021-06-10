#!/usr/bin/python3
'''
author: Tobias Weis
'''

from cpppo.server.enip import client
from cpppo.server.enip.get_attribute import proxy_simple
import time
import numpy as np
import sys

#with client.connector(host='192.168.124.16', timeout=2) as connection:
#    print(connection)

# SMV Inverter controller, Assembly 100:
# Word 0
#   Bit 0 - Forward (0/1)
#   Bit 1 - Reverse (0/1)
#   Bit 2 - Fault reset transition
#   Bit 3 - N/A
#   Bit 4 - N/A
#   Bit 5 - Local control (0) vs Network Control (1)
#   Bit 6 - Local Speed reference (0) vs Network speed reference (1)
#   Bit 7 - N/A
#   Bit 8,9,10,11 - Network speed reference 
#   Bit 12 - No Action (0) vs. Coast to Stop (1)
#   Bit 13 - No Action (0) vs. Quick Stop (1)
#   Bit 14 - No Action (0) vs. Force Manual Mode (1)
#   Bit 15 - DC brake active (0) vs. DC brake NOT active (1)


# Output Assembly 21 - Extended Speed Control
# Bit   0       0/1 (NOT Forward, forward)
#       1       0/1 (NOT Reverse, reverse)
#       2       Fault reset transition
#       3
#       4
#       5
#       ...
#       16-32   Speed in RPM

# we want to set word0 to:
#print(int('1000000001100001', 2)) # forward, network speed ref, no brake
#print(int('1000000001100000', 2)) # network speed ref, no brake
#print(np.ushort(int('1000000001100000', 2)))

# stop 
#print(int('0001000000000000', 2)) # not forward, Coast to Stop, dc brake active

with proxy_simple("192.168.124.16") as via1, proxy_simple("192.168.124.17") as via2:
    print("================================")
    print("Starting drive")

    # forward, network speed ref, no brake
    data, = via1.read([('@4/21/3=(UINT)%d,80' % np.ushort(int('0000000001100001', 2)), 'UINT')])
    print(data)

    data, = via2.read([('@4/21/3=(UINT)%d,180' % np.ushort(int('0000000001100001', 2)), 'UINT')])
    print(data)


    print("================================")
    print("Reading back values")

    # read again
    for via in [via1, via2]:
        print("Assembly 21")
        data, = via.read([('@4/21/3', 'UINT')])
        print(data)
        for d in data:
            print('{0:16b}'.format(d))

        print("Assembly 101")
        data, = via.read([('@4/101/3', 'UINT')])
        print(data)
        for d in data:
            print('{0:16b}'.format(d))

    time.sleep(15)

    print("================================")
    print("Stop drive")


    # reset
    for via in [via1, via2]:
        data, = via.read([('@4/21/3=(UINT)%d,0' % np.ushort(int('0000000000000000', 2)), 'UINT')])
        print(data)

    print("================================")
    print("Reading back values")

    # read again
    for via in [via1, via2]: 
        print("Assembly 100")
        data, = via.read([('@4/100/3', 'UINT')])
        print(data)
        for d in data:
            print('{0:16b}'.format(d))

        print("Assembly 101")
        data, = via.read([('@4/101/3', 'UINT')])
        print(data)
        for d in data:
            print('{0:16b}'.format(d))




'''
import logging
import sys
import time
import threading

from cpppo.server.enip import poll
from cpppo.server.enip.get_attribute import proxy_simple as device
params                  = [
                                ('@1/0/1','UINT'), # Identity Object - Class 0x01, Instance 0, Attribute 1 - Revision (=1)
                                ('@1/1/1','UINT'), # Identity Object - Class 0x01, Instance 1, Attribute 1 - Vendor Id (=587)
                                ('@1/1/2', 'UINT'), # Device Type (=2)
                                ('@1/1/7','SSTRING'), # Identity Object - Class 0x01 (1)
                                ('@4/100/3','UINT'), # Assembly Object - 0x04, Instance 100, Attributes: 3 for DATA Get/Set 
                                #('@4/100/2','DINT'), 
                                #('@4/100/3','DINT'), 
                                #('@4/100/4','DINT'), 
                                #('@4/107/3','INT'), 
                                #('@4/106/3','DINT'), 
                                #('@4/100/3', 'DINT'),
                                #('@4/20/3', 'DINT')
                                ]


hostname                = '192.168.124.16'
values                  = {} # { <parameter>: <value>, ... }
poller                  = threading.Thread(
    target=poll.poll, args=(device,), kwargs={
        'address':      (hostname, 44818),
        'cycle':        1.0,
        'timeout':      0.5,
        'process':      lambda par,val: values.update( { par: val } ),
        'params':       params,
    })
poller.daemon           = True
poller.start()

# Monitor the values dict (updated in another Thread)
while True:
    while values:
        a = values.popitem()
        print(a)
        for i in range(0,len(a[1])):
            try:
                print(a[1][i])
                print('{0:16b}'.format(int(a[1][i])))
            except:
                pass
        #print(type(a))
        #print('{0:16b}'.format(a[1]))
        #logging.warning( "%16s == %r", *values.popitem() )
    print("----------------")
    time.sleep( .1 )
'''
