# -*- coding: utf-8 -*-
"""
Created on Wed May 17 16:14:50 2023

@author: eliot
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
from forward_methods import outputFE
from rk4_methods import outputRK4
from backward_trapezoidal_methods import outputBE, outputTR 
from whaveshaping_methods import output_static

#Boss DS1 with 1N4148 diodes
#circuit_param = np.array([2000, 0.01*10**-6, 2.52*10**-9, 25.852e-3, 1.752]) #[R, C, Is, Vt, n]

#MXR Disto+ with 1N4148 diodes
circuit_param = np.array([10000, 1*10**-9, 2.52*10**-9, 25.852e-3, 1.752])#[R, C, Is, Vt, n]


A = 2 #amplification factor of the input signal
Freq = 500 #frequency of the sinuisoidal input signal
tmax = 2/Freq #simulation time 

overSamplingFactor = 16
Fs = 44100
Fs*=overSamplingFactor

Ts = 1/Fs

n = np.arange(round(Fs*tmax))

#input signal
Vi = A*np.sin(2*np.pi*Freq*n*Ts)

#output signal generated with different methodes
VoTR = outputTR(Vi, Ts, circuit_param)
VoBE = outputBE(Vi, Ts, circuit_param)
VoStatic = output_static(Vi)

#Not stable methods !!
#VoFE = outputFE(Vi, Ts, circuit_param)
#VoRK4 = outputRK4(Vi, Ts, circuit_param)


fig, ax = plt.subplots()

ax.plot(n*Ts, Vi,'r--',alpha=0.5, label='Input signal')
ax.plot(n*Ts, VoTR,'k', label='Trapezoidal')
ax.plot(n*Ts, VoBE,'b--', label='Backward Euler')
ax.plot(n*Ts, VoStatic,'g',alpha=0.8, label='Static Approch')

ax.set_title('Diode Clipping simulation with different methods')
ax.set_xlabel('Time [s]')
ax.set_ylabel('Amplitude [V]')
ax.legend()
ax.grid()
