# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 21:59:03 2023

@author: eliot
"""

import numpy as np
import matplotlib.pyplot as plt

def g(u, v, R, C, Is, Vt, eta):
    return (u-v)/(R*C)-2*Is/C*np.sinh(v/(eta*Vt))

def outputRK4(Vi, Fs, circuit_param):
    R, C, Is, Vt, eta = circuit_param

    
    if len(Vi)% 2 == 0:
        
        Vo = np.zeros(int(len(Vi)/2))
        Vo[0]= 0
        T = 2/Fs
        
        for i in range(len(Vo)-1):
            k1 = T*g(Vi[(i*2)],   Vo[i],      R, C, Is, Vt, eta)
            k2 = T*g(Vi[(i*2)+1], Vo[i]+k1/2, R, C, Is, Vt, eta)
            k3 = T*g(Vi[(i*2)+1], Vo[i]+k2/2, R, C, Is, Vt, eta)
            k4 = T*g(Vi[(i*2)+2], Vo[i]+k3,   R, C, Is, Vt, eta)
            
            Vo[i+1] = Vo[i] + k1/6 + k2/3 + k3/3 + k4/6 
            
        return Vo

    else :
        return print('''Erreur ! Le nombre d'échantillon du signal entrant doit être pair!''')




if __name__ == "__main__":

    circuit_param = np.array([10000, 1*10**-9, 2.52*10**-9, 25.85e-3, 1.752]) #[R, C, Is, Vt, eta]
    
    overSamplingFactor = 100
    Fs = 44100
    Fs*=overSamplingFactor
    
    
    Ts = 1/Fs
    tmax = 0.012 #simulation time in second
    n = np.arange(round(Fs*tmax))
    
    
    A = 1 #gain provide by the OPA to the input signal
    Freq = 147 #frequency of the input signal
    
    #input amplified signal
    Vi = A*np.sin(2*np.pi*Freq*n*Ts)
    
    
    Vo = outputRK4(Vi, Fs, circuit_param)

    

    fig, ax = plt.subplots()
    
    t = n*Ts
    
    
    
    #ax.plot(t, Vi,'r--',alpha=0.5, label='Input signal')
    ax.plot(t[::2], Vo,'k',alpha=0.5, label='Output signal')

    
    
    ax.set_title('Diode Clipping simulation with Trapezoidal Rule')
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Amplitude [V]')
    ax.legend()
    ax.grid()
    
    
    #write("test_TR.wav", Fs, Vo.astype(np.int32))