import telnetlib
import time
import datetime


multimeter_address ="192.168.1.1"
#setup telnet
multimeter = telnetlib.Telnet()
#initialize the multimeter with the given settings
multimeter.open(multimeter_address,port=3490,timeout=3)
#set the multimeter into remote mode
multimeter.write(("SYST:REM\n").encode('ascii'))


print('start :  {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
try:
    for i in range(60):
        multimeter.write(("MEAS:VOLT:DV?\n").encode("ascii"))
        voltage= multimeter.read_eager()
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
