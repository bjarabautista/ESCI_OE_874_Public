import numpy as np
from numpy import exp, sqrt, log, log10
import matplotlib.pyplot as plt

# Absorption
# this functions is based on
# Ainslie M. A., McColm J. G., "A simplified formula for viscous and 
# chemical absorption in sea water", Journal of the Acoustical Society of 
# America, 103(3), 1671-1672, 1998.
# Semme J. Dijkstra November 11, 2019

# C2.1.0 The Absorption Function
def absorption( t=None,d=None,s=None,pH=None,f=None):
    # t: temp in C
    # d: Depth in m
    # s: Salinity in PSU
    # pH: acidity 
    # f: Central Frequency in Hz - this may be an array
    

    # C2.1.1 Scale the Units
    d /= ...
    f /= ...
    
    # C2.1.2 Testing the Conditions 
    if not -6 < t < 35:
        raise RuntimeError('absorption.absorption: Temperature out of range!')
    if not -7.7 < pH < 8.3:
        raise RuntimeError('absorption.absorption: ...')
    if not ...:
        raise RuntimeError('absorption.absorption: salinity out of range!')
     
    try:
        if not 0 < d.all() < 7:
            ...
    except:
        ...

    # C2.1.3 Viscous Absorption Generated by Particle Motion
    a=0.00049*f**2*exp(-(.../27+.../17))

    # C2.1.4 Boric acid Relaxation Frequency
    f1=0.78*sqrt(...)*exp(...)

    # C2.1.5 Magnesium Sulphate Relaxation Frequency
    f2=...

    # C2.1.6 Ainslie and McColm Simplified Formula: Boron
    a += ...*f1*f**2/(...)*exp(...)
    
    # C2.1.7 Ainslie and McColm Simplified Formula: Magnesium Sulphate
    a += .52*...*...*...*exp(...)
    
    # return the result
    return a

def absorption_draw(verbose = True):
    t = 20                       # temp in C
    d = 3.5                      # Depth in km
    s = 35                       # Salinity in PSU
    pH = 8                       # acidity 
    f_log = np.arange(-1,3.1,.1) #  log10( central frequency [kHz])
    f = 10**f_log                # Central frequency in kHz
    

    
    # This method plot some graphs to hopefully help your understanding of the behavior of absorption
    fig = plt.figure(figsize=(18, 6))
    fig.suptitle("Ainslie and McColm (1998) Simplified Absorption Model")
    
    ax0 = fig.add_subplot(1, 3, 1)
    ax1 = fig.add_subplot(1, 3, 2)
    ax2 = fig.add_subplot(1, 3, 3)
    
    # in the first plot we hold all values other than the frequency fixed (the 'classic' presentation)
    # This plot mimics the one found at:
    # http://resource.npl.co.uk/acoustics/techguides/seaabsorption/physics.html 
    # Determine the relaxation frequencies for Boron (f1) and Magnesium Sulfate (f2) for the conditions
    f1=0.78*sqrt(s/35)*exp(t/26)
    f2=42*exp(t/17)

    # Determine the Absorption Generated by Particle Motion (pure water)
    a_pure = 0.00049 * f**2 * exp(-(t/27+d/17))
    
    # Determine the Absorption Generated by Boron
    a_boron = 0.106*f1*f**2/(f1**2+f**2)*exp((pH-8)/.56)
    
    # Determine the Absorption Generated by Magnesium Sulfate
    a_MgSO_4 = .52*(1+t/43)*s/35*f2*f**2/(f2**2+f**2)*exp(-d/6)
    
    # The total absorption
    a_total = a_pure + a_boron + a_MgSO_4
    ax0.plot(f,a_pure,'cyan', label = 'Pure water')
    ax0.plot(f,a_boron,'red', label = 'Boric acid')
    ax0.plot(f,a_MgSO_4,'green', label = 'Magnesium sulfate')
    ax0.plot(f,a_total,'black', label = 'Total absorption')
    ax0.set_xscale("log")
    ax0.set_yscale("log")
    ax0.set_title('Absorption vs Frequency')
    ax0.grid('True')
    ax0.legend()
    ax0.set_xlabel('Frequency [kHz]' )
    ax0.set_ylabel('Absorption [dB/km]' )
    ax0.set_xlim((np.min(f), np.max(f)))
    ax0.set_ylim((10**-6, 10**4))

    if verbose:
        print( "Parameters used for left figure")
        print( "Depth      : %.1fkm"%d)
        print( "Temperature: %.1f\u00B0C"%t)
        print( "PS         : %.1fppt"%s)
        print( "pH level   : %.1f"%pH)
    
    # In the 2nd plot we will compare the total absorption of 4 geographic locations
    # using the numbers from Table 1 from Ainslie & McColm, 1998. 
    oceans = ['Pacific Ocean', 'Red Sea', 'Arctic Ocean', 'Baltic Sea']
    pH_levels = [7.7, 8.2, 8.2, 7.9]
    salinities = [34, 40, 30, 8]
    temperatures = [4, 22, -1.5, 4]
    depths = [1.0, 0.2, 0, 0]
    
    for n, pH, s, t, d in zip(oceans, pH_levels, salinities, temperatures, depths):
        
        if verbose:
            print( "\nParameters used for %s"%n)
            print( "Depth      : %.1fkm"%d)
            print( "Temperature: %.1f\u00B0C"%t)
            print( "PS         : %.1fppt"%s)
            print( "pH level   : %.1f"%pH)
        
        # Just a repeat from before, but with the different values
        f1=0.78*sqrt(s/35)*exp(t/26)
        f2=42*exp(t/17)
        a = 0.00049 * f**2 * exp(-(t/27+d/17))
        a += 0.106*f1*f**2/(f1**2+f**2)*exp((pH-8)/.56)
        a += .52*(1+t/43)*s/35*f2*f**2/(f2**2+f**2)*exp(-d/6)
        
        ax1.plot(f,a,label = n)
    
    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.set_title('Absorption in Different Oceans')
    ax1.grid('True')
    ax1.legend()
    ax1.set_xlabel('Frequency [kHz]' )
    ax1.set_ylabel('Absorption [dB/km]' )
    ax1.set_xlim((np.min(f), np.max(f)))
        

    # In the 3d plot we hold all values other than the depth fixed, 
    # This to illustrate the effect of depth
    f = 100                  # Central frequency in kHz
    d = np.arange(0,7,.01)   # Depth in km
    
    # Determine the Absorption Generated by Particle Motion (pure water)
    a_pure = 0.00049 * f**2 * exp(-(t/27+d/...))
    
    # Determine the Absorption Generated by Boron
#     a_boron = 0.106*f1*f**2/(f1...+f...)*exp((pH-8)/...)
    
    # Determine the Absorption Generated by Magnesium Sulfate
#     a_MgSO_4 = .52*(1+t/...)*s/35*f2*f.../(f2...+f...)*exp(-d/6)
    
    # The total absorption
    a_total = a_pure + a_boron + a_MgSO_4
    
    if verbose:
        print( "Parameters used for Right figure")
        print( "Central F  : %.1fkHz"%f)
        print( "Temperature: %.1f\u00B0C"%t)
        print( "PS         : %.1fppt"%s)
        print( "pH level   : %.1f"%pH)

    # Plot the depth vs absorption dependence
    ax2.plot(d,a_total,'black', label = 'Total absorption')
    ax2.set_title('Absorption vs Depth')
    ax2.grid('True')
    ax2.legend()
    ax2.set_xlabel('Depth [km]' )
    ax2.set_ylabel('Absorption [dB/km]' )
    ax2.set_xlim((np.min(d), np.max(d)))

    

