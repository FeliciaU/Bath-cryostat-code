import telnetlib
import time
import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import re
###Notes from Felica###
#b'+9.90000000E+37\r\n'
#+9.90000000E+37
#This is the open circuit value for any measurements
#Set multimeter to DHCP and hard reset.
#Might have to change the IP to closer to your computer IP.









# multimeter.write(("*cls\n").encode('ascii'))
# self.get_error()
# multimeter.write(("SYST:REM\n").encode('ascii'))
# time.sleep(1)
# self.get_error()
# multimeter.write(("MEAS:VOLT:DC?\n").encode("ascii"))
# time.sleep(1)
# print(multimeter.read_eager())
# self.get_error()
# multimeter.write(("MEAS:VOLT:DC?\n").encode("ascii"))
# time.sleep(1)
# print(multimeter.read_eager())
# self.get_error()

class tektronixDMM4040(object):
    def __init__(self,ip="10.30.128.63"):
        self.ipaddress =ip
        #setup telnet
        self.multimeter = telnetlib.Telnet()
        #initialize the multimeter with the given settings
        self.multimeter.open(self.ipaddress,port=3490,timeout=3)
        #set the multimeter into remote mode
        self.send_command("*cls\n")
        self.get_error()

    def get_error(self):
        self.multimeter.write(("SYST:ERR?\n").encode('ascii'))
        time.sleep(0.2)
        value= self.multimeter.read_eager()
        # value = value.decode("ascii")
        # value = re.search(r'\d.{13}', value)
        if value !=b'+0,"No error"\r\n':
            print(value)
            return(True)

    def send_command(self,command,v=True):
        self.multimeter.write((command).encode('ascii'))
        if v:
            if self.get_error():
                print(command[:-1])


    def setup_fast(self):
        self.send_command("*cls\n")
        #self.send_command("conf:volt:dc 0.1\n")
        self.send_command("conf:res\n")

        self.send_command("zero:auto 0\n")
        self.send_command("trig:sour imm\n")
        self.send_command("trig:del 0\n")
        self.send_command("trig:coun 1\n")
        self.send_command("disp off\n")
        self.send_command("SYST:REM\n")
        self.get_error()

    def collect_data(self,v=True,sample_count=10,integration_time=0.4):
        """
        sample counts can be up to 5000
        integration times are in ms and can ONLY be the following:
        int time=  0.4ms   4ms     20ms    200ms   2000ms
        """
        end=0
        # integration time as nplc/50
        # nplc =    0.02    0.2     1       10      100
        #int time=  0.4ms   4ms     20ms    200ms   2000ms
        integration={0.4:0.02,4:0.2,20:1,200:10,2000:100}
        nplc=integration[integration_time]
        #self.send_command("volt:dc:nplc "+str(nplc)+"\n")
        self.send_command("res:nplc "+str(nplc)+"\n")
        self.send_command("samp:coun "+str(sample_count)+"\n")
        if v:
            print('start :  {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
        start=time.time()
        self.send_command(":INIT; *OPC?\n",v=False)
        for i in range(sample_count+10):
            time.sleep(integration_time/1000)
            value =self.multimeter.read_eager()
            #print(value)
            if value == b'1\r\n' or value == b'\r\n':
                end=time.time()
                if v:
                    print(end-start)
                    print('end   :  {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
                break
            #print(value)

        self.send_command(":FETCH?\n",v=False)
        time.sleep(1)
        value=self.multimeter.read_very_eager()
        if v:
            print(value)
        return end-start




    #closes the multimeter
    def close(self):
        self.get_error()
        self.multimeter.close()


if __name__ == "__main__":
    dmm=tektronixDMM4040("10.30.128.63")
    dmm.setup_fast()
    dmm.collect_data(sample_count=10,integration_time=20)
    dmm.close()
