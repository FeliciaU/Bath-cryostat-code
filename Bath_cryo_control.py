# -*- coding: utf-8 -*-
"""
Created on Wed 20th Sept 2016

@author: feliciaullstad

Power up router. Wait 2 minutes. Connect instruments and computer.
Make sure DHCP is enabled on instrument config.
Check what the ip-addresses of the 3 instruments are, look under instr config on front panel.
$ netstat -nr | grep default

Also check what addresses the arduino and current source are on, they can change when uplugged.
$ ls /dev/tty.*

The sample voltmeter and ammeter are both Tektronix 4040 DMMs.
Can connect via RS232 or ethernet.

The thermometer voltmeter is a FLUKE 8845A multimeter.
Can connect via RS232 or ethernet.

The magnetic field sensor is a Group3 DTM-133 which outputs an analog voltage on the
two back pins which is proportional to the applied field.
This is read by an Ardunio UNO (knock-off) which has a simple analog read and
send serial data setup.

Current source setup:
Keithley 6220 via RS232.
Baudrate 19.2k LF (line feed terminator) No flow control. 8 bits, 1 stop, no parity.
Page 3-15 in manual has programming commands.
Red (high), black (low), green (earth)

"""

import telnetlib
import time
import serial
import os
import sys
import matplotlib as plt
import numpy as np

sample_name='Test24March'
comment='trial'
date=time.strftime("%Y%m%d")
filename=sample_name+'_'+comment+'_'+date+'.txt'

#file_location='/home/feliciaullstad/Desktop/Google_Drive/PhD/SmN data/Bath cryostat/'+sample_name
file_location='/Users/Felicia/Desktop/GoogleDrive/PhD/SmN data/Bath cryostat/'+sample_name


#Also have option to select a sequence
current=1000*10**-6    # Sample current in amps
meas_pause=5    # Seconds between each measurement
end_time=100    # End time in seconds
MAXvoltage=20   #Setting the compliance voltage of sample current source


"""Setup connections to the various devices"""

#Always connect multimeters through the router.
sample_voltmeter_address='192.168.1.66'  #ip address of multimeter TEK COLD
sample_ammeter_address='192.168.1.86'    #ip address of multimeter TEK HOT
thermo_voltmeter_address='192.168.1.67'  #ip address of multimeter FLUKE
sample_currentsource_address='/dev/tty.usbserial'  #serial location of current source on a mac
hall_sensor_address='/dev/tty.wchusbserial620' #Arduino to read voltage from hall probe on a mac

# DO NOT CHANGE BELOW THIS LINE
######################################################

if not os.path.exists(file_location):     #Checks if the python folder exists
    os.makedirs(file_location)            #If not, it makes it

"""Open folder, loop through files, compare names. If match adds a number to the end and keeps running.
This is currently not working. """
n=1
for files in os.listdir(file_location):
    if files==filename:
        #sys.exit('\t A file with this name already exists in this folder. \n \t \t Stopping to avoid overwriting data. \n \t \t Please rename file parameters in preamble.')
        #Maybe rewrite so that it just adds a number to the end of the text file name
        print('This filename already exists, adding a number to the end for you.')
        filename=sample_name+'_'+comment+'_'+date+'_'+str(n)+'.txt'
        n=n+1


"""Setup connections to the various devices"""
sample_voltmeter=telnetlib.Telnet()   #Setup telnet
thermo_voltmeter=telnetlib.Telnet()   #Setup telnet
sample_ammeter=telnetlib.Telnet()   #Setup telnet

#hall_sensor=serial.Serial(port=hall_sensor_address, baudrate=115200, timeout=3)  #Sets up connection to arduino for measuring the magn field

sample_currentsource=serial.Serial(sample_currentsource_address, 19200, bytesize=8, parity='N', stopbits=1, timeout=3)   #Setup serial
sample_currentsource.write(('SYST:REM'+'\n').encode('ascii'))  #
sample_currentsource.write(('CLE'+'\n').encode('ascii'))  #
sample_currentsource.write(('CURR:RANG:AUTO ON'+'\n').encode('ascii'))  #
time.sleep(1)

sample_voltmeter.open(sample_voltmeter_address, port=3490, timeout=3) #Sets up telnet connection to multimeter
sample_voltmeter.write(('SYST:REM'+'\n').encode('ascii'))  #Set multimeter into remote mode
time.sleep(1)

sample_ammeter.open(sample_ammeter_address, port=3490, timeout=3) #Sets up telnet connection to multimeter
sample_ammeter.write(('SYST:REM'+'\n').encode('ascii'))  #Set multimeter into remote mode
time.sleep(1)

thermo_voltmeter.open(thermo_voltmeter_address, port=3490, timeout=3) #Sets up telnet connection to multimeter
thermo_voltmeter.write(('SYST:REM'+'\n').encode('ascii'))  #Set multimeter into remote mode
time.sleep(1)

f=open(file_location+filename,'w')    #Starts a file with the desired filename with the columns below
f.write("Index\tTime (s)\tTemperature (K)\t Thermometer voltage (V)\tSet Current (A)\tCurrent+ (A)\tCurrent- (A)\t Voltage+ (V)\tVoltage- (V)\tField (T)\tResistance (Ohms)\n")


################################################################################
"""Functions for setting or measuring from the various devices"""

def set_current(machine,current,MAXvoltage): # Sets the current source to outpur current with compliance voltage MAXvoltage.
    machine.write(('CURR '+str(current)+'\n').encode('ascii'))
    machine.write(('CURR:COMP '+str(MAXvoltage)+'\n').encode('ascii'))  #
    machine.write(('OUTP ON'+'\n').encode('ascii'))  #


def reset_current(machine):
    machine.write(('OUTP OFF'+'\n').encode('ascii'))

def auto_range(machine):
    machine.write(('MEAS:CURR:DC?'+'\n').encode('ascii')) #Asks multimeter to set to auto range

def meas_current(machine):
    machine.write(('MEAS:CURR:DC?'+'\n').encode('ascii')) #Asks multimeter to measure the current
    time.sleep(0.5)
    current=machine.read_eager()  #Read current from multimeter
    current_str=current.decode('ascii')
    try:
        current_float=float(current_str)
    except ValueError:
        current_float=0
    return current_float

def meas_voltage(machine):
    machine.write(('MEAS:VOLT:DC?'+'\n').encode('ascii')) #Asks multimeter to measure the voltage
    time.sleep(0.5)
    voltage=machine.read_eager()  #Read voltage from multimeter
    voltage_str=voltage.decode('ascii')
    try:
        voltage_float=float(voltage_str)
    except ValueError:
        voltage_float=0
    return voltage_float

def meas_thermo_volt(machine): #needs \n after command
    machine.write(('MEAS:VOLT:DC?'+'\n').encode('ascii'))
    time.sleep(0.5)
    voltage=machine.read_eager()  #Read voltage from multimeter
    voltage_str=voltage.decode('ascii')
    try:
        voltage_float=float(voltage_str)
    except ValueError:
        voltage_float=0
    return voltage_float

def meas_field(machine):
#The arduino is set to send out a voltage. The max number of bits correspond to the maximum voltage.
    reference_voltage=2.424696  #The voltage corresponding to 1 Tesla
    machine.write(('r').encode('ascii'))  #Sends a read command to the arduino to avoid flooding the serial port
    voltage=machine.readline()   #Reads the voltage
    voltage_str=voltage.decode('ascii')
    try:
        voltage=float(voltage_str)
        field=voltage/reference_voltage #Converts voltage to field strength
    except:	#If the voltage is not read properly
        field=0
    return field

def calc_temp(Z):   # Getting temperature from resistasnce of a CERNOX sensor
    def coeff(Z):
        if 56.14<Z<207.4:
            A=[175.524067, -126.037166, 23.963215, -3.779292, 0.747956,-0.16094, 0.030847,-0.007824, 0.004731, -0.000903, 0.002114]
            ZU=2.36967558115
            ZL=1.74321466645
            return [ZU,ZL,A]
        elif 207.4<Z<983.4:
            A=[42.109099, -37.744427, 8.896841, -1.319517, 0.164734, -0.013341, -0.00261, -0.001115, 0.000989, 0, 0]
            ZU=3.0536833274
            ZL=2.26981978194
            return [ZU,ZL,A]
        elif 983.4<Z<26180:
            A=[5.486831, -6.323754, 2.826604, -1.044979, 0.32262, -0.079284, 0.012923, -5.6E-5, -0.001597, 0, 0]
            ZU=4.59635127561
            ZL=2.94137673807
            return [ZU,ZL,A]
        else:
            print('Resistance not in range')
            #raise Exception()
            A=[5.486831, -6.323754, 2.826604, -1.044979, 0.32262, -0.079284, 0.012923, -5.6E-5, -0.001597, 0, 0]
            ZU=4.59635127561
            ZL=2.94137673807
            return [ZU,ZL,A]
    ZU,ZL,A=coeff(Z)
    try:
        Z=np.log10(Z)
    except ValueError:
        print('Incorrect thermometer resistance')
    X=((Z-ZL)-(ZU-Z))/(ZU-ZL)
    T=0
    for i in range(0,len(A)):
        try:
            T=T+A[i]*np.cos(i*np.arccos(X))
        except ValueError:
            print('Could not calculate temperature, incorrect input')
    return T

def close_machines():    #For closing all relevant devices after finished sampling
    machinelist=[sample_voltmeter,thermo_voltmeter,sample_ammeter,sample_currentsource]
    for machine in machinelist:
        machine.close()
    sample_currentsource.write(('OUTP OFF'+'\n').encode('ascii'))

def close_file():    #For closing all relevant devices after finished sampling
    f.close()

    #sample_voltmeter.close()
    #thermo_voltmeter.close()
    #sample_ammeter.close()
    #sample_currentsource.close()
###############################################################################
"""Starting the measurement section"""
"""
#Dummy setup due to inilazation time of multimeters
reset_current(sample_currentsource) #Resets current source
set_current(sample_currentsource,current,MAXvoltage)    #Sets the positive sample current
time.sleep(1)
dummy_value1=meas_current(sample_ammeter)
time.sleep(1)
dummy_value2=meas_voltage(sample_voltmeter)
"""
starttime=time.time()   #Saves the start time

n=0
time.sleep(1)
current_time=0
while current_time<end_time:
    current_time=time.time()-starttime  #Calculates time since start of script
    reset_current(sample_currentsource) #Resets current source
    set_current(sample_currentsource,current,MAXvoltage)    #Sets the positive sample current
    print('Set current')
    time.sleep(5)
    dummy_value1=meas_current(sample_ammeter)
    time.sleep(1)
    dummy_value2=meas_voltage(sample_voltmeter)
    currentplus=meas_current(sample_ammeter)    #Measures the positive sample current
    print('Pos current: ',currentplus, type(currentplus))
    time.sleep(1)
    voltageplus=meas_voltage(sample_voltmeter)  #Measures the positive sample voltage
    print('Pos voltage: ',voltageplus, type(voltageplus))
    time.sleep(meas_pause) #Pauses loop for meas_pause seconds
    reset_current(sample_currentsource) #Resets current source
    #current=current*-1
    time.sleep(1)
    set_current(sample_currentsource,-current,MAXvoltage)   #Set the negative sample current
    time.sleep(1)
    currentminus=meas_current(sample_ammeter)   #Measures the negative sample current
    print('Neg current: ',currentminus, type(currentminus))
    time.sleep(1)
    voltageminus=meas_voltage(sample_voltmeter) #Measures the negative sample voltage
    print('Neg voltage: ',voltageminus, type(voltageminus))
    resistance=(voltageplus-voltageminus)/(currentplus-currentminus)    #Calculates the sample resistance
    print('The resistance is: ',resistance, type(resistance))
    #field=meas_field(hall_sensor)   #Measures the magnetic field
    field=0
    #print('The field is: ',field, type(field))
    thermovoltage=meas_thermo_volt(thermo_voltmeter)    #Measures the thermometer voltage
    temperature=calc_temp(thermovoltage/10**-5)    #Calculates the temperature
    print('The thermometer voltage is: ',thermovoltage, type(thermovoltage))
    print('The temperature is: ',temperature, type(temperature))
    f.write( "%d\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\n" % (n,current_time,temperature,thermovoltage,current, currentplus,currentminus,voltageplus,voltageminus,field,resistance))    #Writes data to file
    f.flush()   #Flushes data out to file to make sure it writes
    n=n+1
    #current=current*-1
    #set up auto updating plotting
    try:
        fig1=plt.figure(1)
        ax=fig1.add_subplot(211)
        plot1=plt.plot(current_time,temperature,'b.')
        plt.xlabel('Time (s)')
        plt.ylabel('Temperature (K)')
        plt.title('Bath cryostat measurements of '+filename)
        plt.subplot(212)
        plot2=plt.plot(temperature,resistance,'r.')
        plt.ylabel('Resistance (Ohm)')
        plt.xlabel('Temperature (K)')
        string='Magnetic field: '+str(field)
        plt.annotate(string, xy=(1,1), xycoords='axes fraction', horizontalalignment='left')
        plt.pause(0.05)
    except:
	    print('Error plotting')
    time.sleep(meas_pause) #Pauses loop for meas_pause seconds

close_machines()
close_file()

"""
Press ctrl+c to interrupt data sampling
type close_machines() in console
"""
