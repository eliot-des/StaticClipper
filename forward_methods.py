# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 21:59:03 2023

@author: eliot
"""

import numpy as np
import matplotlib.pyplot as plt

def f(u, v, R, C, Is, Vt, eta):
    return (u-v)/(R*C)-2*Is/C*np.sinh(v/(eta*Vt))

def outputFE(Vi, Fs, circuit_param):
    R, C, Is, Vt, eta = circuit_param
    
    Vo = np.zeros(len(Vi))
    Vo[0]= 0
    T = 1/Fs
    print(T)
    for i in range(len(Vi)-1):
        Vo[i+1] = Vo[i] + T* f(Vi[i], Vo[i], R, C, Is, Vt, eta)
    return Vo

if __name__ == "__main__":

    circuit_param = np.array([10000, 1*10**-9, 2.52*10**-9, 25.85e-3, 1.752]) #[R, C, Is, Vt, eta]
    
    overSamplingFactor = 40
    Fs = 44100
    Fs*=overSamplingFactor
    
    
    Ts = 1/Fs
    tmax = 0.012 #simulation time in second
    n = np.arange(round(Fs*tmax))
    
    
    A = 4 #gain provide by the OPA to the input signal
    Freq = 147 #frequency of the input signal
    
    #input amplified signal
    Vi = A*np.sin(2*np.pi*Freq*n*Ts)
    
    
    Vo = outputFE(Vi, Fs, circuit_param)



    fig, ax = plt.subplots()
    
    
    ax.plot(n*Ts, Vi,'r--',alpha=0.5, label='Input signal')
    ax.plot(n*Ts, Vo,'r--',alpha=0.5, label='Input signal')

    
    
    ax.set_title('Diode Clipping simulation with Trapezoidal Rule')
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Amplitude [V]')
    ax.legend()
    ax.grid()
    
    
    #write("test_TR.wav", Fs, Vo.astype(np.int32))