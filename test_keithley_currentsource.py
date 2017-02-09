import telnetlib
import time
import serial
import os
import sys
import matplotlib as plt

sample_currentsource_address='/dev/ttyUSB0'  #serial location of current source

sample_currentsource=serial.Serial(sample_currentsource_address, 19200, bytesize=8, parity='N', stopbits=1, timeout=3)   #Setup serial
sample_currentsource.write('*IDN?\r')  #
print(sample_currentsource.readline())

#sample_currentsource.readline()
#sample_currentsource.write('SYST:ERR\n')  #
#sample_currentsource.write('SYST:COMM:SER:CONT:RTS OFF\n')  #

sample_currentsource.write('SYST:REM\n')  #
sample_currentsource.write('CLE\n')  #
sample_currentsource.write('CURR:RANG:AUTO ON\n')  #

MAXvoltage=15   #Setting the compliance voltage of current source
time.sleep(1)

time.sleep(1)



################################################################################
#Functions for setting or measuring from the various devices

def set_current(machine,current,MAXvoltage): # Needs to be rewritten for its instrument
    machine.write('CURR '+str(current)+'\n')
    machine.write('CURR:COMP '+str(MAXvoltage)+'\n')  #
    machine.write('OUTP ON\n')  #


def reset_current(machine):
    machine.write('OUTP OFF')
    print(7)

set_current(sample_currentsource,12e-3,MAXvoltage)
