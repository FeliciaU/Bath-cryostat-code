

hall_sensor_address='/dev/ttyUSB1'

hall_sensor=serial.Serial(port=hall_sensor_address, baudrate=115200)  #Sets up connection to arduino for measuring the magn field



def meas_field(machine):
    maxbits=1023    #Number of bits corresponding to 5V on the arduino serial reader
    reference_voltage=2.43  #The voltage corresponding to 1 Tesla
    voltage_bits=machine.read_eager()   #Reads the voltage as a bit value between 0 and 1023
    voltage=voltage_bits/maxbits*5  #Converts bit value to voltage
    field=voltage/reference_voltage #Converts voltage to field strength
    return field


for i in range(10):
    field=meas_field(hall_sensor)
    print(field)
