#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 19:30:03 2020

@author: pablitolito

Python script to calculate average values per site for parameters saved in tables 
created by A1.get_NRM-Components_fromRemasoft_v2024. 
It iterates through the files and looks for matching site names to compute the averages.

To run the script, place it in the directory where the files previously created with A1 are located. 
It will automatically find the files based on the beginning of the filename and perform the calculations.

Notes:
    - If the filenames have been changed, they will not be found.
    - If there is more than one component in the Summary_Components files, 
      it will mix the information for both. Therefore, clean the files beforehand 
      (without changing the comma-separated format).
    - Change the delimiter (site_delimiter) between the site name and specimen name 
      according to your data. The default is "-".

Output:
    A comma-separated file with a table showing the average values per site.ç
"""

import numpy as np
import csv
from os import listdir

site_delimiter='-' #change the - by your own delimiter between site and specimen name

def get_T_coer(row):
    #Estrae los valores de Tmin, Tmax, Coercitividad min, Coer Max de cada muestra
    #Si no hay Temperatura o Coercitividad, lo deja vacío
    if 'C' in row[15]:
        tmin=[int(row[15][:-1])]
        tmax=[int(row[16][:-1])]
        cmin, cmax=[], []
    elif 'mT' in row[15]:
        tmin, tmax=[], []
        cmin=[int(row[15][:-2])]
        cmax=[int(row[16][:-2])]
    else:
        tmin, tmax=[], []
        cmin, cmax=[], []
        
    return tmin, tmax, cmin, cmax

def calc_T_C_mean(tmin_t,tmax_t,cmin_t,cmax_t):
    #Calcula las medias de las cuatro listas si hay valores, si no, pone 'Nan'
    tmin_mean = round(np.mean(tmin_t), 1) if tmin_t else 'Nan'
    tmax_mean = round(np.mean(tmax_t), 1) if tmax_t else 'Nan'
    cmin_mean = round(np.mean(cmin_t), 1) if cmin_t else 'Nan'
    cmax_mean = round(np.mean(cmax_t), 1) if cmax_t else 'Nan'
    
    return tmin_mean, tmax_mean, cmin_mean, cmax_mean


def get_data_comp(file):
    # Process component files to compute mean values for NRM and Component intensities,
    # as well as for temperatures and coercivities
    data_out = [['Site', 'n', 'NRM_comp_mean_(A/m)', 'stdev', 
             'Comp_mean_(A/m)', 'stdev', 'n_Th', 'n_AF', 
             'Tmin_mean(C)', 'Tmax_mean(C)', 
             'Coerc-min_mean(mT)', 'Coerc-max_mean(mT)']]

    data = np.genfromtxt(file, dtype='str', delimiter=',', skip_header=1, usecols=range(17))
    name_i = data[0][0].split('-')[0]

    nrm_t, comp_t, tmin_t, tmax_t, cmin_t, cmax_t = [], [], [], [], [], []
    
    for row in data:
        name=row[0].split(site_delimiter)[0]
        
        if name==name_i:
            try:
                nrm_t.append(float(row[5]))
            except ValueError:
                print(f'Error with {row[0]} NRM value in the Summary_Components file')
            try:
                comp_t.append(float(row[7]))
            except ValueError:
                print(f'Error with {row[0]} component value')
            try:
                tmin,tmax,cmin,cmax=get_T_coer(row)
                tmin_t.extend(tmin)
                tmax_t.extend(tmax)
                cmin_t.extend(cmin)
                cmax_t.extend(cmax)
            except ValueError:
                print(f'Error with {row[0]} temperature or coercivity values')
        else:
            data_out.append([name_i, len(comp_t), np.mean(nrm_t), np.std(nrm_t), 
                             np.mean(comp_t), np.std(comp_t), len(tmin_t), len(cmin_t), 
                             *calc_T_C_mean(tmin_t, tmax_t, cmin_t, cmax_t)])
            name_i, nrm_t, comp_t, tmin_t, tmax_t, cmin_t, cmax_t = name, [float(row[5])], [float(row[7])], *get_T_coer(row)

    data_out.append([name_i, len(comp_t), np.mean(nrm_t), np.std(nrm_t), 
                     np.mean(comp_t), np.std(comp_t), len(tmin_t), len(cmin_t), 
                     *calc_T_C_mean(tmin_t, tmax_t, cmin_t, cmax_t)])
    return data_out
    
def get_data_nrm(file):
    # Processes NRM files to compute mean and standard deviation of intensities (NRM_comp)
    data_out = [['Site', 'n', 'NRM_comp_mean_(A/m)', 'stdev']]
    data = np.genfromtxt(file, dtype='str', delimiter=',', skip_header=1, usecols=(0, 5))
    
    name_i = data[0][0].split('-')[0]
    nrm_t = []
    
    for row in data:
        name=row[0].split('-')[0]
        
        if name==name_i:
            try:
                nrm_t.append(float(row[1]))
            except ValueError:
                print(f'Error with {row[0]} NRM value')
        else:
            data_out.append([name_i, len(nrm_t), np.mean(nrm_t), np.std(nrm_t)])
            name_i, nrm_t = name, [float(row[1])]

    data_out.append([name_i, len(nrm_t), np.mean(nrm_t), np.std(nrm_t)])
    
    return data_out
    

nrm_names = [f for f in listdir(".") if f.startswith('NRM_')]
comp_names = [f for f in listdir(".") if f.startswith('Summary_Components_')]
        
print(f'NRM files name: {nrm_names}')
print(f'Components files name: {comp_names}')

for file in comp_names:
    data_out = get_data_comp(file)
    name_out = f'Mean_Int_{file[:-4]}.txt'
    with open(name_out, 'w', newline='') as file_out:
        writer = csv.writer(file_out)
        writer.writerows(data_out)
        
        
for file in nrm_names:
    data_out = get_data_nrm(file)
    name_out = f'Mean_Int_{file[:-4]}.txt'
    with open(name_out, 'w', newline='') as file_out:
        writer = csv.writer(file_out)
        writer.writerows(data_out)

