import numpy as np
from numpy import log, log10, sqrt
from om_math import incoherent_sum_log10

## NoiseLevel - Function estimating Noise Level based the Wenz curves
# Based on USNL Lecture notes found at:
# https://www.usna.edu/Users/physics/ejtuchol/documents/SP411/Chapter11.pdf
# On November 6, 2016 (Underwater Acoustics and Sonar SP411 Handouts and
# Notes Fall 2006)


# Semme J. Dijkstra  November 6,2016

def noise_level( s_s,s_d,fc,bw,verbose):
    # Initialization - this is only so that the students have something to compare to
    nl_1k = 0
    f = np.zeros(2)
    nl_ship = np.zeros(2)
    nl_surf = np.zeros(2)
    nl = 0
    
    # SS: Sea State
    # SD: Shipping density as ranging [1,7]

    # C4.0 Noise Levels 10-100Hz:  NL_100
    if s_d < 1 or s_d > 7:
        raise RuntimeError('noise_level.noise_level: shipping density out of range')
    nl_100 = 60 + (s_d - 1) * 5
    
    # C4.2 Noise Level 1000Hz:  NL_1K
    if s_s ==0:
        nl_1k = 44.5
    elif s_s <= 0.5:
        nl_1k = 50

    elif s_s <= 1:
        nl_1k = 55
    elif s_s <= 2:
        nl_1k = 61.5

    elif s_s <= 3:
        nl_1k = 64.5
    elif s_s <= 4:
        nl_1k = 66.5
    
    elif s_s <= 5:
        nl_1k = 68.5
    else:
        nl_1k=70

    # C4.5 Calculating the Lower and Upper Cut-Off Frequency of the Band
    f = np.zeros(2)
    f[0] = (sqrt((4*fc**2)+(bw**2))-bw)/2
    f[1] = f[0]+bw
    
    # C4.6 Calculataing the Noise for the Lower-  and Upper-Cutoff Frequencies $f_1$ and $f_2$
    for i in range(2):
        if f[i] < 10**1:
            raise RuntimeError('NL: function not implemented for frequencies < 10 Hz')

        elif 10**1 <= f[i] and f[i] < 10**2:
            nl_ship[i] = nl_100
            nl_surf[i] = nl_1k
        elif 10**2 <= f[i] and f[i] < 10**3:
            nl_ship[i]=nl_100 - 20 * log10(f[i] / 10**2)
            nl_surf[i] = nl_1k
        elif 10**3 <= f[i] and f[i] < 10**5:
            nl_ship[i]=nl_100 - 20 * log10(f[i] / 10**2)            
            nl_surf[i] = nl_1k-17 * log10(f[i] / 10**3)
        else:
            raise RuntimeError('NL: function not implemented for frequencies > 100 kHz')

    # C4.7 Determining the Levels for the Entire Signal
    nl_surf_band = sum(nl_surf)/2+10*log10(bw)
    nl_ship_band = sum(nl_ship)/2+10*log10(bw)

    # C4.9 Determine the Total Noise Level
    nl = incoherent_sum_log10((nl_surf_band, nl_ship_band))

    if verbose:
        # Let the user know what was found
        print('NL_100                               : %.1f dB re. 1 uPa'%nl_100)
        print('NL_1K                                : %.1f dB re. 1 uPa'%nl_1k)
        print('Lower cutoff frequency               : '+ str(f[0])+' Hz')
        print('Upper cutoff frequency               : '+ str(f[1])+' Hz')
        print('Shipping noise (Urick,1986)          : %.1f dB re. 1 uPa'%nl_ship_band)
        print('Surface noise (Knudsen, 1984)        : %.1f dB re. 1 uPa'%nl_surf_band)
        print('Total Ambient noise                  : '+ str(nl)+' dB re. 1 uPa')

    return nl 
        
        
        