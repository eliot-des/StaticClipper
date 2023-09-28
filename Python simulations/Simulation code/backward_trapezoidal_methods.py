# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 21:59:03 2023

@author: eliot
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
import time

def f_fderiv_BE(Vo, Vo_old, Vi, Ts, circuit_param):
    
    R, C, Is, Vt, neta = circuit_param
    Vt*=neta
    
    f = Vo_old - Vo + Ts*(((Vi-Vo)/(R*C)) - (2*Is*np.sinh(Vo/Vt))/C)
    deriv_f = -Ts*(((2*Is*np.cosh(Vo/Vt))/(C*Vt))+1/(R*C))-1
    return f, deriv_f

def f_fderiv_TR(Vo, Vo_old, Vi, Vi_old, Ts, circuit_param): 
    
    R, C, Is, Vt, n = circuit_param
    Vt*=n
    
    f = Vo_old - Vo + (Ts/2)*(((Vi+Vi_old-Vo-Vo_old)/(R*C)) - (2*(Is/C)*(np.sinh(Vo/Vt)+np.sinh(Vo_old/Vt))))
    deriv_f = -(Ts/2)*(((2*Is*np.cosh(Vo/Vt))/(C*Vt))+1/(R*C)) - 1
    return f, deriv_f


def newtowRaphson_BE( a, b, Ts, circuit_param, relative_error=1e-6):
    
    x = a #initial condition to compute the Newtow's method 
            #Interesting to change this value by a random float or by 
            #the previous sample of Vo which is a in this setup to see how 
            #it affect the computing time.
            
    x_old = 100 #intentionally high to enter in the while loop
                #will correspond to the precedent x calculus.

    while not np.isclose(x, x_old, rtol=relative_error):

        x_old = x
        f_x, deriv_f_x  = f_fderiv_BE(Vo=x, Vo_old=a, Vi=b, Ts=Ts, circuit_param = circuit_param)
        x = x - (f_x/deriv_f_x)
        
    return x

def newtowRaphson_TR(a, b, c, Ts, circuit_param, relative_error=1e-6):
    
    x = a #initial condition to compute the Newtow's method 
            #Interesting to change this value by a random float or by 
            #the previous sample of Vo which is a in this setup to see how 
            #it affect the computing time.
            
    x_old = 100 #intentionally high to enter in the while loop
                #will correspond to the precedent x calculus.

    while not np.isclose(x, x_old, rtol=relative_error):
        x_old = x
        f_x, deriv_f_x  = f_fderiv_TR(Vo=x, Vo_old=a, Vi=b, Vi_old= c, Ts=Ts, circuit_param = circuit_param)
        x = x - (f_x/deriv_f_x)
    return x
    

def outputBE(Vi, Ts, circuit_param):

    Vo = np.empty(len(Vi))
    Vo[0] = Vi[0]  #initial condition of the output signal -> valuable if the first value is below the clipping threshold
    
    for i in range(1,len(Vi)):
        
        Vo[i] = newtowRaphson_BE(a=Vo[i-1], b=Vi[i], Ts = Ts, circuit_param = circuit_param)
    
    return Vo

def outputTR(Vi, Ts, circuit_param):

    Vo = np.empty(len(Vi))
    Vo[0] = Vi[0]  #initial condition of the output signal -> valuable if the first value is below the clipping threshold
    
    for i in range(1,len(Vi)):
        
        Vo[i]= newtowRaphson_TR(a=Vo[i-1], b=Vi[i], c=Vi[i-1], Ts = Ts, circuit_param=circuit_param)
    
    return Vo


if __name__ == "__main__":


    circuit_param = np.array([10000, 1*10**-9, 2.52*10**-9, 25.852e-3, 1.752]) #[R, C, Is, Vt, n]
    
    overSamplingFactor = 100
    Fs = 44100
    
    Fs*=overSamplingFactor
    
    
    Ts = 1/Fs
    tmax = 0.012 #simulation time in second
    n = np.arange(round(Fs*tmax))
    
    A = 1 #gain provide by the OPA to the input signal
    Freq = 147 #frequency of the input signal
    
    #input amplified signal
    Vi = A*np.sin(2*np.pi*Freq*n*Ts)#+A*np.sin(2*np.pi*155*n*Ts)
    
    
    
    VoTR = outputTR(Vi, Ts, circuit_param)
    VoBE = outputBE(Vi, Ts, circuit_param)
    
    
    fig, ax = plt.subplots()
    
    
    ax.plot(n*Ts, Vi,'r--',alpha=0.5, label='Input signal')
    ax.plot(n*Ts, VoTR,'k', label='Output TR')
    ax.plot(n*Ts, VoBE,'b--', label='Output BE')
    
    
    ax.set_title('Diode Clipping simulation with Trapezoidal Rule')
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Amplitude [V]')
    ax.legend()
    ax.grid()
    
    
    #write("test_TR.wav", Fs, Vo.astype(np.float32))