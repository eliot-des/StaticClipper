# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 17:16:06 2023

Just a test for WDF Method, can contain errors

@author: garamburo - eliot.des
"""

import numpy as np
import matplotlib.pyplot as plt
plt.close('all')

# Settings
Fs = int(48e3*16)
Ts = 1 / Fs

# Time Domain Variables
T = 0.1
N = int(Fs * T)
t = np.arange(N)/Fs
fs = 1000
x = 1*np.sin(2 * np.pi * fs * t)
y = np.zeros(N)

# Components
R = 2.2e4
C = 0.47e-6

# WD Impedance
Zc = Ts / (2 * C)
mC = 0

# Diode 1N4148 Characteristics
Is = 2.52e-9
Vt = 25.85e-3
eta = 1
eta_Vt = eta * Vt
Rs = 1e-3
Rp = 1e9

# Adaptors
Zs1 = R + C
ks1 = R / Zs1

# Omega
def w3(x):
    x1 = -3.341459552768620
    x2 = 8.
    a = -1.314293149877800e-3
    b = 4.775931364975583e-2
    c = 3.631952663804445e-1
    d = 6.313183464296682e-1
    if x < x1:
        return 0
    else:
        if x < x2:
            return d + x * (c + x * (b + x * a))
        else:
            return x - np.log(x)


def w4(x):
    y = w3(x)
    return y - (y - np.exp(x - y)) / (y + 1.)

def DiodeRoot(a, Z):
    Z_inv = 1 / Z
    sig = (1 + Rs * Z_inv) / (2 * eta_Vt)
    lam = a * (1 - Rs * Z_inv) / (2 * eta_Vt)
    ka = - (1 + Z_inv * (Rs + Rp)) / (2 * Is * Rp)
    mu = 1 - a * (1 - Z_inv * (Rs + Rp)) / (2 * Is * Rp)
    b = -w4(lam - sig * (mu / ka) + np.log(- sig / ka)) / sig - mu / ka
    return b

for n in range(N):
    # Wave Up
    as1 = -x[n] - mC
    
    # Root
    b = DiodeRoot(np.abs(as1), Zs1) * np.sign(as1)
    
    # Output
    y[n] = -(b + as1)/2
    
    # Wave down
    mC = mC*ks1 + b*(ks1-1)
    
plt.figure()
plt.title('Diode Clipping Y/X')
plt.ylabel('Output [V]')
plt.xlabel('Input [V]')
plt.grid()
plt.plot(x, y)
plt.tight_layout()
plt.show()

plt.figure()
plt.title('Diode Clipping Input & Output')
plt.ylabel('Voltage [V]')
plt.xlabel('Time [s]')
plt.grid()
plt.plot(t, x, label = 'Input')
plt.plot(t, y, label = 'Output')
plt.xlim((3*4/fs, 4*4/fs))
plt.legend()
plt.tight_layout()
plt.show()