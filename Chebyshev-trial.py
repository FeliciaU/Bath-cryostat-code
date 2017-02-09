import numpy.polynomial.chebyshev as chebyshev
import math

#coefs are ZL, ZU, A(0), A(1), A(2),A(3), A(4), A(5), A(6), A(7), A(8), A(9)
#coef_2_12K=[1.32412,1.69812,7.556358,-5.917261,0.237238,-0.334636,-0.058642,-0.019929,-0.020715,-0.014814,-0.008789,-0.008554]
coef_100_475K=[0.079767,0.999614,287.756797,-194.144823,-3.837903,-1.318325,-0.109120,-0.393265,0.146911,-0.111192,0.028877,-0.029286,0.015619]
Voltage=0.37337 # This will be a measured value later
x=((Voltage-coef_100_475K[0])-(coef_100_475K[1]-Voltage))/(coef_100_475K[1]-coef_100_475K[0])

Temp=0
for index in range(9):
    print(x)
    p=index*math.acos(x)
    print(p)
    t=math.cos(p)
    print(t)
    addition=t*coef_100_475K[index+2]
    Temp=Temp+addition

print(Temp)
