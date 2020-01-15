#THL_DAC_SCAN#
##################################
# THL Scan with medipix devices.
# Take a dac scan over range of THL and create a spectrum

# Section 1: load file, plot spectrum and integral.
# Section 2: Fit curve with gaussian, Find position of peaks and the FWHM of peaks
# Section 3: Plot error due to charge sharing. FInd standard dev, standard error, average count, and average differential count.
###################################

import numpy as np
from numpy import loadtxt
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp
from scipy.signal import savgol_filter
import pickle
from pypeaks import Data, Intervals

###################################
# section 1
###################################


FilenamePrefix = 'AMdactest2.1_THLFine_'  #To make filename that we will call to use
                           #ex "test_2.1_THLFine_101.txt" is file name
                           #Prefix = 'test_2.1_THLFine_'

THLstart = 100           #begining of interested thl range
THLstop = 598             #end of the interested thl range
THLlength = THLstop - THLstart + 1

FBK = 128                  #Default value is 128, check the dac control panel for the value


THLVECT= []                #initialize arrays
datList=[]

print("Files used in spectrum: ")

for n in range(THLlength): ##range(start, stop, step)
    THLVAL = THLstart + n
    THLVECT.append(THLVAL)
    filename = "{}{}_iToT.txt" .format(FilenamePrefix,THLVAL)
    print(filename)
    dat = np.loadtxt(filename, usecols=range(256))
    mat = dat.flatten()
    datcount = np.sum(mat)
    datList.append(datcount)

# now we have two lists:
# THLVECT which is each of the ascending THL values
# and datList which is each summed element from acquisition
# next we differentiate datList using gradient
# so that we won't need to subtract an element

diffDAT = np.gradient(datList)
# print(datList)            #optional check

# next we plot the spectrum

plt.plot(THLVECT,diffDAT)
plt.xlabel("THL [ARB]")
plt.ylabel(r'$\frac{DN}{DE}$')
plt.title(' Global Spectrum from Measurement #s  {} to {}'.format(THLstart, THLstop))
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
#ax = plt.gca()
#ax.invert_xaxis()          #depeding on polarity of device you will want to invert the x axis
plt.show()                  #with inversion for positive polarity (check?)

#plot the integral THL vs  counts


plt.plot(THLVECT,datList)
plt.xlabel("THL [ARB]")
plt.ylabel('N')
plt.title('integral of measured spectrum')
# ax = plt.gca()
# ax.invert_xaxis()
plt.show()

#sarajilic paper suggests to plot THL-FBK against diff counts
#here is that version of spectrum

# print (type(THLVECT))
# print (type(FBK))
THLFBK = np.asarray(THLVECT) - FBK
plt.title('THL-FBK vs DN/DE')
plt.plot(THLFBK,diffDAT)
plt.xlabel("THL-FBK")
plt.ylabel(r'$\frac{DN}{DE}$')
plt.grid()
plt.show()

###################################
# section 2
###################################
x = THLVECT
y = diffDAT

#appy Savitzky-Golay filter to data if noisy
                        #argument (data,windowsize,poly-order)
yfilt = savgol_filter(y,11,3)

plt.plot(x,y)
plt.plot(x,yfilt)
plt.title('smoothed curve')
plt.legend()
plt.grid()
plt.show()
# fit a gaussian on the plot,
# make sure to change y to yfilt
# if you want the smoothed data
y = yfilt



                         # find arithmetic mean
peak_val = y.max()
mean = x[y.argmax()]
sigma= mean - np.where(y > peak_val* np.exp(-.5))[0][0]

Text = 'mean = {0:.3f} and sigma = {1:.3f}'.format(mean,sigma)

def Gauss(x, a, x0, sigma):
    return a * np.exp(-(x - x0)**2 / (2 * sigma**2))

popt,pcov = curve_fit(Gauss, x, y, p0=[peak_val, mean, sigma])

plt.plot(x, y, 'b+:', label='data')
plt.plot(x, Gauss(x, *popt), 'y-', label='fitted curve')
plt.legend()
plt.title(' Global Spectrum Fit from Measurement #s  {} to {}'.format(THLstart, THLstop))
plt.xlabel("THL [ARB]")
plt.ylabel(r'$\frac{DN}{DE}$')
plt.xlim(400,550)
plt.grid()
plt.show()

print(Text)

# find other peaks and their FWHM,
# pypi lets you smooth in function.
# I opt to customize argument and apply the filter previous to this step

##currently under dev~~~~

# peaks, _ = find_peaks(y)
# results_half = peak_widths(x, peaks, rel_height=0.5)
# print(results_half[0])

# data_obj = Data(x, y, smoothness=1)
# data_obj.get_peaks(method='slope')
# data_obj.plot()

##################################
# section 3
###################################
#apply charge sharing corrections
#create csv with pertinant values
#such as mu, sigma, multiple peaks
