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

plt.style.use('default')
plt.rcParams.update({'font.size': 40})
plt.rcParams.update({'legend.fontsize': 35})
plt.rcParams.update({'lines.linewidth': 5})
plt.rcParams.update({'lines.markersize': 25})




directory='comparaison_experience'



circuit_param = np.array([10000, 1*10**-9, 2.52*10**-9, 25.85e-3, 1.752])

overSamplingFactor = 8
Fs = 48000
Fs*=overSamplingFactor


Ts = 1/Fs
tmax = 10#simulation time in second
n = np.arange(round(Fs*tmax))
t = n*Ts

A = 1 #gain provide by the OPA to the input signal
freq = 3000 #frequency of the input signal

#input amplified signal
Vi = A*np.sin(2*np.pi*freq*n*Ts)



#VoFE  = outputFE(Vi, Fs, circuit_param)
#VoBE  = outputBE(Vi, Fs, circuit_param)
#VoTR  = outputTR(Vi, Fs, circuit_param)
#VoRK4 = outputRK4(Vi, Fs, circuit_param)

VoWhave= output_static(Vi)
#write(f"{directory}//FE_{A}v_{freq}Hz_{tmax}s_{int(Fs/1000)}kHz.wav", Fs, VoFE.astype(np.float32))
#write(f"{directory}//BE_{A}v_{freq}Hz_{tmax}s_{int(Fs/1000)}kHz.wav", Fs, VoBE.astype(np.float32))
#write(f"{directory}//TR_{A}v_{freq}Hz_{tmax}s_{int(Fs/1000)}kHz.wav", Fs, VoTR.astype(np.float32))
#write(f"{directory}//RK4_{A}v_{freq}Hz_{tmax}s_{int(Fs/1000)}.wav", int(Fs/2), VoRK4.astype(np.float32))


write(f"{directory}//Sculteur d'onde_{A}v_{freq}Hz_{tmax}s_{int(Fs/1000)}kHz.wav", Fs, VoWhave.astype(np.float32))

'''
fig, ax = plt.subplots()


#ax.plot(t, Vi,'r--',alpha=0.5, label='Input signal')

ax.plot(t, VoTR,'k', label='Output TR')
ax.plot(t, VoBE,'b--', label='Output BE')
#ax.plot(t, VoFE,'g', label='Output FE')
#ax.plot(t[::2], VoRK4,'r--', label='Output RK4')
ax.legend()
'''
