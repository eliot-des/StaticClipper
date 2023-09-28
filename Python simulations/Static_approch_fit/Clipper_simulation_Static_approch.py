# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 21:20:44 2023

@author: eliot
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
#print(plt.style.available)

plt.style.use('default')
plt.rcParams.update({'font.size': 40})
plt.rcParams.update({'legend.fontsize': 45})
plt.rcParams.update({'lines.linewidth': 7})
plt.rcParams.update({'lines.markersize': 25})


plt.close('all')
#0.01*10**-6

#[10000, 1*10**-9, 2.52*10**-9, 25.852e-3, 1.752]

def f_fderiv_Static(Vo, Vi, R=10000, C=1*10**-9, Is=2.52*10**-9, Vt=25.85e-3, n=1.752):
    """
    

    Parameters
    ----------
    Vo : float64
        Output signal sample, correspond to Vo[n].
    Vi : float64
        Input signal sample, correspond to Vi[n].
    R : float, optional
        Resistance value (Ohms). The default is 5.
    C : float, optional
        Capacitor value (Farads). The default is 0.01*10**-6.
    Is : float, optional
        Inverse Bias Current of one diode (Ampheres). The default is 2.5e-9.
    Vt : TYPE, optional
        Thermal voltage value of one diode (Volts). The default is 25e-3.

    Returns
    -------
    f : 
        function of Vo.
    deriv_f :
        Derivative of f(Vo).

    """
    
    Vt*=n
    
    f = ((Vi - Vo)/(R*C)) - 2*(Is/C)*np.sinh(Vo/Vt, dtype=np.float64)
    deriv_f = (-1/(R*C)) - ((2*Is)/(C*Vt))*np.cosh(Vo/Vt, dtype=np.float64)


    return f, deriv_f


def newtowRaphson(b, relative_error=1e-10):
    
    x = b #initial condition to compute the Newtow's method 
            #Interesting to change this value by a random float or by 
            #the previous sample of Vo which is a in this setup to see how 
            #it affect the computing time.
            
    x_old = 1000 #intentionally high to enter in the while loop
                #will correspond to the precedent x calculus.

    while not np.isclose(x, x_old, rtol=relative_error):
        
        x_old = x
        
        f_x, deriv_f_x  = f_fderiv_Static(Vo=x, Vi=b)
        
        x = x - (f_x/deriv_f_x)
    return x
    
    
def output(Vi):
    """
    

    Parameters
    ----------
    Vi : array
        1D numpy array of the input signal.

    Returns
    -------
    Vo : array
        1D numpy array of the output signal.

    """
    
    Vo = np.empty(len(Vi))

    for i in range(0,len(Vi)):
        
        Vo[i]= newtowRaphson(b=Vi[i])
    
    return Vo



def tanh_approx(Vi, n =2.5):

    return np.array([x/((1+abs(x)**n)**(1/n)) for x in Vi ])
    

def tanh_approx2(x,L, n):
    return x*L/((1+abs(x)**n)**(1/n)) 
    

def sigmoid(x,L,a, n=2.5):
     y = x*L/((1+abs(x)**n)**(a/n))
     return y
 
def sigmoid2(x, a, b, x0, k):
     y = a + b/(1 + np.exp(-k*(x-x0))) #tester avec un coefficient à la place de l'exponentielle
     return y
 
def sigmoid3(x, a, b, c, n):
     y = x*a/((1+abs(c*x)**n)**(b/n))
     return y



#input amplified signal
Vi_max = 5

Vi = np.linspace(-Vi_max ,Vi_max ,1000)
Vo = output(Vi)



#polynomial fit
pfit_order = 30
poly_list = np.polyfit(Vi, Vo, pfit_order)
polyfit_func = np.poly1d(poly_list)

#sigmoid fit
#popt, pcov  = curve_fit(sigmoid, Vi, Vo)
popt2,pcov2 = curve_fit(sigmoid2,Vi,Vo)
popt3,pcov3 = curve_fit(sigmoid3,Vi,Vo)
popt4,pcpv4 = curve_fit(tanh_approx2,Vi,Vo)

for n in range(len(popt3)):
    print(popt3[n])

for n in range(len(popt2)):
    print(popt2[n])
    
#Vo_sigmoid  = sigmoid(Vi,*popt)
Vo_sigmoid2 = sigmoid2(Vi,*popt2)
Vo_sigmoid3 = sigmoid3(Vi,*popt3)


Vo_tanh_approx2 = tanh_approx2(Vi,*popt4)
'''
fig, ax = plt.subplots(2,1,figsize=(20,15),sharex=True,gridspec_kw={'height_ratios': [3, 2]}, layout='constrained')

ax[0].plot(Vi, Vo,'k',                  label="Fonction NR")


#[0].plot(Vi, polyfit_func(Vi),'r',    label='Approx. polyfit (order : {})'.format(pfit_order))
#ax[0].plot(Vi, np.tanh(Vi),             label='tanh')
#ax[0].plot(Vi, np.arctan(Vi),             label='atan')
#ax[0].plot(Vi, np.arctan(Vi)-Vo ,             label='atan diff')
#ax[0].plot(Vi, Vo_tanh_approx2, 'c--',  label='tanh approx')
ax[0].plot(Vi, Vo_sigmoid3 ,'r--',      label=r'Sigmoïde 1 $w_1(V_i)$' )
ax[0].plot(Vi, Vo_sigmoid2 ,'--',color='steelblue',      label='Sigmoïde 2 $w_2(V_i)$' )
#ax[0].plot(Vi, Vo_sigmoid ,'m--',       label='Approx. sigmoid 3 fit' )



#ax[1].plot(Vi,20*np.log10(abs((Vo-polyfit_func(Vi))/Vo)),'r',    label='polyfit')
ax[1].plot(Vi,20*np.log10(abs((Vo-Vo_sigmoid3)/Vo)),'r',       label='Sigmoïde $w_1(V_i)$' )
ax[1].plot(Vi,20*np.log10(abs((Vo-Vo_sigmoid2)/Vo)),color='steelblue',       label='Sigmoïde $w_2(V_i)$')
#ax[1].plot(Vi,20*np.log10(abs((Vo-Vo_sigmoid)/Vo)),'m',        label='sigmoid 3 fit' )


#ax[1].plot(Vi,20*np.log10(abs((Vo-Vo_tanh_approx2)/Vo)),'c--',   label='tanh approx fit ')

ax[0].set_title("""Fonctions sculteuses d'onde - Approche Statique""")
ax[1].set_title("""Erreur relative par rapport à Newton-Raphson""")
ax[1].set_xlabel(r'$V_i $ [V]')
ax[0].set_ylabel(r'$V_o $ [V]')
ax[1].set_ylabel(r'|Erreur| [dB]')
#ax[0].set_yticks(np.arange(-0.6,0.7,0.2))
ax[1].set_ylim(-100,5)

for i in range(2):
    ax[i].grid(True)
    ax[i].set_xlim(-Vi_max,Vi_max)
    ax[i].legend(loc='upper left')

#plt.savefig("test.png", transparent=True)

'''
fig, ax = plt.subplots(figsize=(20,15), layout='constrained')

ax.plot(Vi, Vo,'k',                  label='Fonction Newton')

ax.plot(Vi, Vo_sigmoid3 ,'c--',      label='Sigmoïde 1 fit' )
ax.plot(Vi, Vo_sigmoid2 ,'b--',      label='Sigmoïde 2 fit' )


ax.set_title("""Fonctions sculteuses d'onde - Approche Statique""")

ax.set_xlabel(r'$V_i $ [V]')
ax.set_ylabel(r'$V_o $ [V]')


ax.grid(True)
ax.set_xlim(-Vi_max,Vi_max)
ax.legend(loc='upper left')

