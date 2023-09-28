# -*- coding: utf-8 -*-
"""
Created on Wed May 17 16:14:50 2023

@author: eliot
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
from forward_methods import outputFE
from backward_trapezoidal_methods import outputBE, outputTR 
from rk4_methods import outputRK4

A = 4 #gain provide by the OPA to the input signal
Freq = 147 #frequency of the input signal

tmax = 0.005 #simulation time in second


circuit_param = np.array([10000, 1*10**-9, 2.52*10**-9, 25.85e-3, 1.752]) #[R, C, Is, Vt, eta]


overSamplingFactor = 80
Fs = 44100
Fs*=overSamplingFactor


Ts = 1/Fs
n = np.arange(round(Fs*tmax))
t = n*Ts



#input amplified signal
Vi = A*np.sin(2*np.pi*Freq*n*Ts)



VoFE  = outputFE(Vi, Fs, circuit_param)
VoBE  = outputBE(Vi, Fs, circuit_param)
VoTR  = outputTR(Vi, Fs, circuit_param)
VoRK4 = outputRK4(Vi, Fs, circuit_param)


fig, ax = plt.subplots()


ax.plot(t, Vi,'r--',alpha=0.5, label='Input signal')

ax.plot(t, VoTR,'k', label='Output TR')
ax.plot(t, VoBE,'b--', label='Output BE')
ax.plot(t, VoFE,'g', label='Output FE')
ax.plot(t[::2], VoRK4,'r--', label='Output RK4')
ax.legend()
ax.grid()