import serial
import time
hall_sensor_address='/dev/ttyUSB0'

hall_sensor=serial.Serial(port=hall_sensor_address, baudrate=9600, timeout=3)  #Sets up connection to arduino for measuring the magn field
time.sleep(1)


def meas_field(machine):
#The arduino is set to send out a voltage. The max number of bits correspond to the maximum voltage.
    reference_voltage=2.424696  #The voltage corresponding to 1 Tesla
    machine.write('r')
    voltage=machine.readline()   #Reads the voltage
    try:
	    voltage=float(voltage)
	    field=voltage/reference_voltage #Converts voltage to field strength
    except:	#If the voltage is not read properly
	   field=0
    return field


for i in range(15):
    field=meas_field(hall_sensor)
    print(field)
    time.sleep(0.5)
