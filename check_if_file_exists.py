
import os
import time
import sys


'''
Set up to check if filename already exists
'''

"""Measuring setup"""

sample_name='F27'
comment='trial'
date=time.strftime("%Y%m%d")
filename=sample_name+'_'+comment+'_'+date+'.txt'
current=1*10**-7    # Sample current in amps
meas_pause=5    # Seconds between each measurement
end_time=100    # End time in seconds
file_location='/home/feliciaullstad/Desktop/GoogleDrive/PhD/SmN data/Bath cryostat/'+sample_name
######################################################

if not os.path.exists(file_location):     #Checks if the python folder exists
    os.makedirs(file_location)            #If not, it makes it

"""Open folder, loop through files, compare names. If match prompt error """
for file in os.listdir(file_location):
    if file==filename:
        sys.exit('\t A file with this name already exists in this folder. \n \t \t Stopping to avoid overwriting data. \n \t \t Please rename file parameters in preamble.')

f=open(file_location+'/'+filename,'w')    #Starts a file with the desired filename with the columns below
f.write("Index\tTime (s)\tTemperature (K)\t Temperature voltage (V)\tSet Current (A)\tCurrent+ (A)\tCurrent- (A)\t Voltage+ (V)\tVoltage- (V)\tResistance (Ohms)\n")
