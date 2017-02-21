import telnetlib
import time
import datetime

#b'+9.90000000E+37\r\n'
#+9.90000000E+37
#This is the open circuit value for any measurements
#Set multimeter to DHCP and hard reset. Might have to change the IP to closer to your computer IP.

multimeter_address ="169.254.112.87"
#setup telnet
multimeter = telnetlib.Telnet()
#initialize the multimeter with the given settings
multimeter.open(multimeter_address,port=3490,timeout=3)
#set the multimeter into remote mode
multimeter.write(("SYST:REM\n").encode('ascii'))


print('start :  {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
try:
    for i in range(60):
        multimeter.write(("MEAS:VOLT:DC?\n").encode("ascii"))
        voltage= multimeter.read_eager()
        print(voltage)
        voltage = voltage.decode("ascii")
        print(voltage)
        time.sleep(1)
except KeyboardInterrupt:
    print('end   :  {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
    multimeter.close()
    print(time)


print('end   :  {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
#closes the multimeter
multimeter.close()
