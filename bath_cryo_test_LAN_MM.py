# -*- coding: utf-8 -*-
"""
Created on Wed 20th Sept 2016

@author: feliciaullstad

The sample voltmeter and ammeter are both Tektronix 4040 DMMs

The thermometer voltmeter is a FLUKE 8845A multimeter
Can connect via RS232 or ethernet


Current source setup:
This might have to be rewritten depending on what current source is
Keithley 6220 via RS232.
Baudrate 19.2k LF (line feed terminator) No flow control. 8 bits, 1 stop, no parity.
Page 3-15 in manual has programming commands


"""

import telnetlib
import time
import serial
import os
import sys

sample_name='TEST'
comment='trial'
date=time.strftime("%Y%m%d")
filename=sample_name+'_'+comment+'_'+date+'.txt'

file_location='/home/feliciaullstad/Desktop/Google_Drive/PhD/SmN data/Bath cryostat/'+sample_name

#Also have option to select a sequence
current=1*10**-7    # Sample current in amps
meas_pause=5    # Seconds between each measurement
end_time=10    # End time in seconds

# DO NOT CHANGE BELOW THIS LINE
######################################################

if not os.path.exists(file_location):     #Checks if the python folder exists
    os.makedirs(file_location)            #If not, it makes it

"""Open folder, loop through files, compare names. If match prompt error and close program """
for file in os.listdir(file_location):
    if file==filename:
        sys.exit('\t A file with this name already exists in this folder. \n \t \t Stopping to avoid overwriting data. \n \t \t Please rename file parameters in preamble.')




"""Setup connections to the various devices"""
sample_voltmeter_address='10.30.128.255'  #ip address of multimeter
sample_ammeter_address='10.30.128.158'
thermo_voltmeter_address='10.30.128.196'  #ip address of multimeter


sample_voltmeter=telnetlib.Telnet()   #Setup telnet
sample_ammeter=telnetlib.Telnet()   #Setup telnet
thermo_voltmeter=telnetlib.Telnet()   #Setup telnet

sample_voltmeter.open(sample_voltmeter_address, port=3490, timeout=3) #Sets up telnet connection to multimeter
sample_voltmeter.write('SYST:REM\n')  #Set multimeter into remote mode
time.sleep(1)

sample_ammeter.open(sample_ammeter_address, port=3490, timeout=3) #Sets up telnet connection to multimeter
sample_ammeter.write('SYST:REM\n')  #Set multimeter into remote mode
time.sleep(1)

thermo_voltmeter.open(thermo_voltmeter_address, port=3490, timeout=3) #Sets up telnet connection to multimeter
thermo_voltmeter.write('SYST:REM\n')  #Set multimeter into remote mode
time.sleep(1)



################################################################################
"""Functions for setting or measuring from the various devices"""


def meas_current(machine):
    machine.write('MEAS:CURR:DC?\n') #Asks multimeter to measure the current
    current=machine.read_eager()  #Read current from multimeter
    return current

def meas_voltage(machine):
    machine.write('MEAS:VOLT:DC?\n') #Asks multimeter to measure the voltage
    voltage=machine.read_eager()  #Read voltage from multimeter
    return voltage

def meas_thermo_volt(machine): #needs \n after command
    machine.write('MEAS:VOLT:DC?\n')
    voltage=machine.read_eager()  #Read voltage from multimeter
    return voltage


def close_all():    #For closing all relevant devices after finished sampling
    f.close()
    sample_voltmeter.close()
    thermo_voltmeter.close()
    sample_ammeter.close()
    #sample_currentsource.close()
###############################################################################

starttime=time.time()   #Saves the start time
f=open(filename,'w')    #Starts a file with the desired filename with the columns below
f.write("Index\tTime (s)\t Thermometer voltage (V)\t Current- (A)\t Voltage- (V)\t Resistance (Ohms)\n")

n=0
time.sleep(1)
current_time=0
while current_time<end_time:
    current_time=time.time()-starttime  #Calculates time since start of script
    voltageminus=meas_voltage(sample_voltmeter)
    currentminus=meas_current(sample_ammeter)
    #resistance=(voltageminus)/(currentminus)
    resistance=1
    thermovoltage=meas_thermo_volt(thermo_voltmeter)
    #thermovoltage=1
    print(voltageminus)
    print(currentminus)
    print(thermovoltage)
    print(' ')
    #f.write( "%d\t%f\t%f\t%f\t%f\t%f\n" % (n,current_time,thermovoltage,currentminus,voltageminus,resistance))    #Writes data to file
    #f.flush()   #Flushes data out to file to make sure it writes
    n=n+1
    #set up auto updating plotting
    time.sleep(1)

close_all()

"""
Press ctrl+c to interrupt data sampling
type telenet.close() and
f.close()
in console
"""
