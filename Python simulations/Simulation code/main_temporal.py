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
from whaveshaping_methods import output_static


#Boss DS1 with 1N4148 diodes
#circuit_param = np.array([2000, 0.01*10**-6, 2.52*10**-9, 25.852e-3, 1.752]) #[R, C, Is, Vt, n]


#MXR Disto+ with 1N4148 diodes
circuit_param = np.array([10000, 1*10**-9, 2.52*10**-9, 25.852e-3, 1.752])#[R, C, Is, Vt, n]


A = 1 #gain applied to the signal at the input of the clipping stage
Freq = 4000 #frequency of the input signal


overSamplingFactor = 32
Fs = 44100
Fs*=overSamplingFactor


Ts = 1/Fs
tmax = 2/Freq #simulation time in second
n = np.arange(round(Fs*tmax))



#input amplified signal
Vi = A*np.sin(2*np.pi*Freq*n*Ts)



VoTR = outputTR(Vi, Ts, circuit_param)
VoBE = outputBE(Vi, Ts, circuit_param)
VoFE = outputFE(Vi, Ts, circuit_param)

fig, ax = plt.subplots()


ax.plot(n*Ts, Vi,'r--',alpha=0.5, label='Input signal')
ax.plot(n*Ts, VoTR,'k', label='Output TR')
ax.plot(n*Ts, VoBE,'b--', label='Output BE')
ax.plot(n*Ts, VoFE,'g', label='Output FE')



ax.set_title('Diode Clipping simulation with different methods')
ax.set_xlabel('Time [s]')
ax.set_ylabel('Amplitude [V]')
ax.legend()
ax.grid()