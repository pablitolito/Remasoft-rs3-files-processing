#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 18:51:15 2020

@author: pablitolito

Python script to create a frequency histogram of NRM intensity.

It searches the folder for files generated by A1.get_NRM-Components_fromRemasoft_v2024.py,
named NRM_DIRECTORY.txt, which are comma-delimited tables.

You can change the lower and upper limits of the x-axis for the histogram,
as well as the number of bins. To do this, modify the variables `lim_inf_x`, `lim_sup_x`, and `bins`.
By default, these are set to the minimum and maximum NRM values and 50 bins.
"""

import numpy as np
import matplotlib.pyplot as plt
from os import listdir


# Function to generate the relative cumulative frequency curve
def ecdf(sample):

    # convert sample to a numpy array, if it isn't already
    sample = np.atleast_1d(sample)

    # find the unique values and their corresponding counts
    quantiles, counts = np.unique(sample, return_counts=True)

    # take the cumulative sum of the counts and divide by the sample size to
    # get the cumulative probabilities between 0 and 1
    cumprob = np.cumsum(counts).astype(np.double) / sample.size

    return quantiles, cumprob


def plot_hist(file_name):
    print(f'\n{file_name} file')
    
    # Read the file and extract data
    nrm=np.genfromtxt(file_name, dtype='float', delimiter=',', skip_header=1, usecols=5)*1000
    
    # Change x-axis limits and bins here
    lim_inf_x=min(nrm)
    lim_sup_x=max(nrm)
    bins=50
    
    fig, ax1=plt.subplots()
    ax2=ax1.twinx()
    
    # Apply the 'ecdf' function and obtain cumulative curve values
    qe, pe = ecdf(nrm)
    
    # Calculate min, max, and quartiles 1, 2, 3 (25%, 50%, and 75%)
    n= 'n = '+str(len(nrm))
    print (n)
    min_nrm=min(nrm)
    max_nrm=max(nrm)
    print('min_nrm: ', min_nrm)
    print('max_nrm: ', max_nrm)
    q1=np.percentile(nrm,25)
    q2=np.percentile(nrm,50)
    q3=np.percentile(nrm,75)
    print('quartile 1: ', q1)
    print('quartile 2: ', q2)
    print('quartile 3: ', q3)
    
    # Draw the histogram
    ax1.hist(nrm,bins=10**np.linspace(np.log10(lim_inf_x),np.log10(lim_sup_x), bins))
    ax1.set_xscale("log")
    ax1.set_ylabel('frequency',color='blue')
    ax1.tick_params('y', colors='blue')
    ax1.set_xlabel('$\ mA/m $')
    
    # Draw the cumulative curve for ChRM intensity
    ax2.plot(qe, pe, '-r')
    ax2.set_ylabel('Cumulative Frequency', color='r', fontsize=12)
    ax2.tick_params('y', colors='r', labelsize=12)
    ax2.set_xscale("log")
    # Add vertical lines for the quartiles
    for q, label in zip([q1, q2, q3], ['25%', '50%', '75%']):
        ax2.axvline(x=q, ymax=0.92, color='k', ls='--')
        ax2.text(q, 0.98, label, ha='center')
    
    # Set title and limit the x-axis to the value specified above
    plt.title('Intensity of the NRM     '+n)
    plt.xlim(lim_inf_x, lim_sup_x, emit=True)
    
    # Save the plot
    plt.savefig(f'Hist_{file_name[:-4]}.pdf')
    plt.savefig(f'Hist_{file_name[:-4]}.png')
    plt.show()

# Get all *.txt files in the current directory that start with 'NRM_'
nrm_names = [f for f in listdir(".") if f.startswith('NRM_') and f.endswith('txt')]
print(f'NRM files: {nrm_names}')
for file in nrm_names:
    plot_hist(file)

