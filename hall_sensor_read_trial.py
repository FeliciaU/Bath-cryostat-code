import serial
import time
#hall_sensor_address='/dev/tty.wchusbserial410'
hall_sensor_address='/dev/tty.usbserial-A900abu3' #Arduino Duemilanove to read voltage from hall probe on a mac

hall_sensor=serial.Serial(port=hall_sensor_address, baudrate=9600, timeout=3)  #Sets up connection to arduino for measuring the magn field
time.sleep(1)


def meas_field(machine):
#The arduino is set to send out a voltage. The max number of bits correspond to the maximum voltage.
    reference_voltage=1.733422 #2.424696  #The voltage corresponding to 1 Tesla
    machine.write(('r').encode('ascii'))
    voltage=machine.readline()   #Reads the voltage
    voltage_str=voltage.decode('ascii')
    print('voltage_str=',voltage_str)
    try:
        voltage=float(voltage_str)
        field=voltage/reference_voltage #Converts voltage to field strength
    except:	#If the voltage is not read properly
        #print('Hi')
        field=0
    return field


for i in range(100):
    field=meas_field(hall_sensor)
    print('field=',field)
    time.sleep(1)
