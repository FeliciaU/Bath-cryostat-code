# -*- coding: utf-8 -*-
"""
Created on Fri 24th March 2017

@author: feliciaullstad

Current source setup:
Keithley 6220 via RS232.
Baudrate 19.2k LF (line feed terminator) No flow control. 8 bits, 1 stop, no parity.
Page 3-15 in manual has programming commands.
Red (high), black (low), green (earth)

"""

import time
import serial
import numpy as np


#Also have option to select a sequence
current=1000*10**-6    # Sample current in amps
meas_pause=5    # Seconds between each measurement
end_time=100    # End time in seconds
MAXvoltage=20   #Setting the compliance voltage of sample current source


"""Setup connections to the various devices"""
sample_currentsource_address='/dev/tty.usbserial'  #serial location of current source on a mac

sample_currentsource=serial.Serial(sample_currentsource_address, 19200, bytesize=8, parity='N', stopbits=1, timeout=3)   #Setup serial
sample_currentsource.write(('SYST:REM'+'\n').encode('ascii'))  #
sample_currentsource.write(('CLE'+'\n').encode('ascii'))  #
sample_currentsource.write(('CURR:RANG:AUTO ON'+'\n').encode('ascii'))  #
time.sleep(1)

################################################################################
"""Functions for setting or measuring from the various devices"""

def set_current(machine,current,MAXvoltage): # Sets the current source to outpur current with compliance voltage MAXvoltage.
    machine.write(('CURR '+str(current)+'\n').encode('ascii'))
    machine.write(('CURR:COMP '+str(MAXvoltage)+'\n').encode('ascii'))  #
    machine.write(('OUTP ON'+'\n').encode('ascii'))  #


def reset_current(machine):
    machine.write(('OUTP OFF'+'\n').encode('ascii'))

def read_error(machine):
    machine.write(('STAT:QUE'+'\n').encode('ascii'))

read_error(sample_currentsource)
sample_currentsource.write(('STAT:CLE'+'\n').encode('ascii'))
"""
Press ctrl+c to interrupt data sampling
type close_machines() in console
"""
