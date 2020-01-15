import numpy as np
from numpy import loadtxt
import matplotlib.pyplot as plt
###THIS CODE IS UNDER-DEV ; taking a while due to the unknown nature of the spectra saved file -oooooowwwooooowwwooooo- mysterious and annoying. ###

# load file, spectrum image from Measurement-> Spectra  file output "save spectra"
#def SpectraView():
FN = 'spectrumimg.txt'                    #give filename as saved from Pixet
spect = np.loadtxt(FN)                    # opt. arg. ,usecols=range(#)
type(spect)
len = len(spect)
print(len)
vects = spect.flatten()

NonZ = np.nonzero(vects)
print(NonZ)

plt.hist(NonZ)
plt.ylabel('Energy Deposit Value [pp]')
plt.xlabel('Number of pixels with certain range value')
plt.show()

