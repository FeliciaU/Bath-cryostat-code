# -*- coding: utf-8 -*-
"""
Created on Mon May 30 14:00:12 2016

@author: feliciaullstad
"""

import telnetlib
import time
"""
Connct switch to network. Connect instruments. MAke sure DHCP is enabled on instrument config.
(In terminal type: sudo ifconfig eth0 169.254.1.200 broadcast 169.254.255.255 netmask 255.255.0.0)
Only if your computer is unhappy with the set ip.
"""

host='192.168.1.66'  #Check on DMM what the ip address actually is.

telnet=telnetlib.Telnet()
telnet.close()  #closes previos session if there was one

telnet.open(host, port=3490, timeout=3)
telnet.write(('SYST:REM'+'\n').encode('ascii'))
n=0
time.sleep(1)
while n<=100:
    telnet.write(('MEAS:RES?'+'\n').encode('ascii'))
    #telnet.write('READ\n')
    print(n,telnet.read_eager())
    time.sleep(0.5)
    n=n+1


telnet.close()
"""
Once you are done you have to close the telnet session, otherwise the next run will be blocked.
"""
