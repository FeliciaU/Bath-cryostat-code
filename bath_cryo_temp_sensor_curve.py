import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import time

def calc_temp(Z):
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
    ZU,ZL,A=coeff(Z)
    Z=np.log10(Z)   #Not sure why this step is here....
    X=((Z-ZL)-(ZU-Z))/(ZU-ZL)
    T=0
    for i in range(0,len(A)):
        T=T+A[i]*np.cos(i*np.arccos(X))
    return T

#----------------------------------------------------------------------------
resistancevector=np.arange(57,26179)
temperature=np.array([])
for resistance in resistancevector:
    temp=calc_temp(resistance)
    temperature=np.append(temperature,temp)
#----------------------------------------------------------------------------
temperature60plus=np.array([])
newresplus=np.array([])
for resistance in resistancevector:
    try:
        temp=calc_temp(resistance*1.02)
        temperature60plus=np.append(temperature60plus,temp)
        newresplus=np.append(newresplus,resistance)
    except:
        print('Not in range')
#----------------------------------------------------------------------------
temperature60minus=np.array([])
newresminus=np.array([])
for resistance in resistancevector:
    try:
        temp=calc_temp(resistance*0.98)
        temperature60minus=np.append(temperature60minus,temp)
        newresminus=np.append(newresminus,resistance)
    except:
        print('Not in range')
#----------------------------------------------------------------------------
temperaturediff=np.array([])
temperaturefordiff=np.array([])
for resistance in resistancevector: # Calculate differences
    try:
        temp=calc_temp(resistance)
        tempplus=calc_temp(resistance*1.02)
        tempdiffplus=abs(temp-tempplus)
        tempminus=calc_temp(resistance*0.98)
        tempdiffminus=abs(temp-tempminus)
        #print(tempdiffminus)
        totaldiff=tempdiffplus+tempdiffminus
        temperaturediff=np.append(temperaturediff,totaldiff)
        temperaturefordiff=np.append(temperaturefordiff,temp)
    except:
        print('Error at resistance'+str(resistance))
#----------------------------------------------------------------------------

fig1=plt.figure()
plot=plt.loglog(resistancevector,temperature,'.',label='Normal')
plot=plt.loglog(newresplus,temperature60plus,'.',label='2 $\%$ plus')
plot=plt.loglog(newresminus,temperature60minus,'.',label='2 $\%$ minus')
plt.ylim(1,340)
#plt.yscale('log', nonposy='clip')
plt.ylabel('Temperature (K)')
plt.xlabel('Resistance ($\Omega$)')
plt.title('Temperature dependent resistance of temp sensor in bath cryostat')
plt.legend(loc=3)
plot=plt.savefig('Bathcryostat_resistance_temp_sensor_2percentplusminus.pdf', format='pdf', dpi=1200)

fig2=plt.figure()
plot=plt.plot(temperaturefordiff,temperaturediff,'.',label='Normal')
#plot=plt.semilogy(temperature60plus,newresplus,'.',label='5 Ohm plus')
#plot=plt.semilogy(temperature60minus,newresminus,'.',label='5 Ohm minus')
plt.xlim(1,340)
#plt.yscale('log', nonposy='clip')
plt.xlabel('Temperature (K)')
plt.ylabel('Temperature difference (max temp-min temp)(K)')
plt.title('Temperature dependent 2 $\%$ error in temp sensor in bath cryostat')
#plt.legend(loc=3)
plot=plt.savefig('Bathcryostat_temp_sensor_2_percent_error.pdf', format='pdf', dpi=1200)

plt.show()
