###eventscanSingle.py



import matplotlib.pyplot as plt
import numpy as np
import glob as glob
import pandas as pd
import os
import astropy.io.ascii
import asciitable
from matplotlib.ticker import StrMethodFormatter

file = "/media/sav/Seagate Portable Drive/Data/MAR6/ACQ1/True_.t3pa"

With = pd.read_table(file)


fileB = "/media/sav/Seagate Portable Drive/Data/MAR6/ACQ2/True_No_.t3pa"

Without = pd.read_table(fileB)

#Create arrays of columns we are interested in 

A1 = With['ToT']
A2 = With['Matrix Index']

B1 = Without['ToT']

			#### Generate ToT vs Matrix Index Plot ###

# plt.scatter(A1,A2,marker = "+")
# plt.xlabel('ToT Periods')# plt.title("ToT vs Matrix Index")
# plt.show()

	##### Generate Histogram of ToT Values
### Note: ToT values are # of periods (25 ns incriment) where an event has registered ( signal energy > THL)
### This creates a histogram of the ToT values as greater # of periods registered in a pixel signifies a greater energy of incident
### signal as the higher energy a particle has, the longer the dissipation time in the Si. 
### Using these assumptions we can say that # of periods are proportional to the energy and we 
### can create a spectrum. 

			##Very bare bones histograms: ##

# With.hist(column = 'ToT', bins = 35, grid = True, figsize = (12,8)) 
# plt.show()

# Without.hist(column = 'ToT', bins = 35, grid = True, figsize = (12,8)) 
# plt.show()

			## See both histograms at once ##


plt.title('Detector Counts with and without Ba133 Present (Bins = 165)')
plt.hist(A1, bins = 265, label = "With Source")
plt.hist(B1, bins = 265, label = "WIthout Source")
plt.legend()
plt.show()


			###### Now lets check the Am241 Trials ######

fileD = "/media/sav/Seagate Portable Drive/Data/MAR6/test2/true_.t3pa"

trial1 = pd.read_table(fileD)

T1 = trial1['ToT']

	#T1 is just the AM241 SOURCE 

fileE = "/media/sav/Seagate Portable Drive/Data/MAR6/test1/True_.t3pa"

trial2 = pd.read_table(fileE)

T2 = trial2['ToT']
	#T2 has glove to stop alpha particles 


#Plotting with and without alphas

plt.title('AM Source With and WIithout Alpha contribution (Bins = 165)')
plt.hist(T1, bins = 265, label = "AM241 Source")
plt.hist(T2, bins = 265, label = "Am241 Without Alphas")
plt.legend()
plt.show()










###### Now lets check the combonation trial ######

fileC = "/media/sav/Seagate Portable Drive/Data/MAR6/combo/true_.t3pa"

Combo = pd.read_table(fileC)

C1 = Combo['ToT']

##BAREBONES MATRIX## 
#Combo.hist(column = 'ToT', bins = 80, figsize = (12,8))
#plt.show()

## Plot alongside : 

plt.figure()
plt.title('Ba + Am, Ba133, Am241 (Bins = 165)')
plt.hist(A1, bins = 265, label = "BA 133") #BA
plt.hist(T1, bins = 265, label = "AM241 Source", alpha = .1)
plt.hist(C1, bins = 265, label = "Combined", alpha = .2) #COMBO
plt.legend()
plt.show()








