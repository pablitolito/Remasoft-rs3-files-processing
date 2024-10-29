#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 13:42:02 2020

@author: pablitolito

The program runs in a directory where subdirectories containing rs3 files are located.

Outputs:
    1. Summary_components_DIRECTORY.txt: Table with calculated components, their intensity, 
       minimum and maximum temperature or coercivities, and corresponding NRM. Specimens 
       without calculated components are not added to the table.
    2. NRM_DIRECTORY.txt: Table with the intensity of the NRM, as well as directional values of the
       specimen (orientation of the specimen and bedding).
"""

import os
import codecs
import csv
import re
from collections import defaultdict

# Traverse subfolders and generate the list of .rs3 files
def get_rs3_files(base_path):
    files_by_folder = defaultdict(list)

    # Traverse all folders and subfolders
    for root_folder, subfolders, files in os.walk(base_path):
        # Get the name of the first subfolder (relative to base_path)
        folder_name = os.path.relpath(root_folder, base_path).split(os.sep)[0]

        # Filter the files with .rs3 extension
        rs3_files = [file for file in files if file.endswith('.rs3')]

        # If there are .rs3 files, add them to the corresponding list
        if rs3_files:
            for rs3_file in rs3_files:
                # Save the full path for each .rs3 file
                file_path = os.path.join(root_folder, rs3_file)
                files_by_folder[folder_name].append(file_path)
                #print(f'file_path: {file_path}')
                
    print(f'files_by_folder: {files_by_folder}')
    return files_by_folder


# Access the .rs3 files, extract their names, and save to .txt files
def save_rs3_info(base_path, files_by_folder):

    # Create the output text files in the script's folder
    for folder, files in files_by_folder.items():
        files.sort()
        # Create a text file with the name of the first subfolder
        output_file_name_comp = f"Summary_Components_{folder}.txt"
        #output_file_path_comp = os.path.join(base_path, output_file_name_comp)  # Save in the base folder
        output_file_name_nrm = f"NRM_{folder}.txt"
        #output_file_path_nrm = os.path.join(base_path, output_file_name_nrm)  # Save in the base folder
        

        nrm_data_out=[['Sample', 'Sdec','Idec','Bdec','BInc','NRM_(A/m)']]
        comp_data_out=[['Sample','Sdec','Idec','Bdec','BInc','NRM_(A/m)',
                   'Component','M(A/m)','Dec_spe','Inc_spe','Dec_geo',
                   'Inc_geo','Dec_tilt','Inc_tilt','MAD','Limit1','Limit2']]        
        
       
        # Iterate over all .rs3 files
        for file_path in files:
            
            nrm_data, comp_data=get_rs3_data(file_path)
            
            
            if len(nrm_data)>0:
                nrm_data_out.append(nrm_data)
            if len(comp_data)>0:
                comp_data_out.extend(comp_data)
            

            
        # Write NRM data to file
        with open(output_file_name_nrm, 'w', encoding='utf-8') as nrm_file_out:
            writer = csv.writer(nrm_file_out, delimiter=',', lineterminator='\n')
            for row in nrm_data_out:
                writer.writerow(row)
        
        # Write component data to file
        with open(output_file_name_comp, 'w', encoding='utf-8') as comp_file_out:
            writer = csv.writer(comp_file_out, delimiter=',', lineterminator='\n')
            for row in comp_data_out:
                writer.writerow(row)
        
    
# Opens each .rs3 file and extracts component information, as well as sample data (NRM, orientation, etc.)
def get_rs3_data(file_name):
    with codecs.open(file_name, encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    cleaned=re.sub(r'[ ]+', ' ', content)
    reader = csv.reader(cleaned.splitlines(), delimiter=' ')
    data=list(reader)
    
    comp_data_out=[]
    nrm_data_out=[]
    info_site = data[1][0:5] + [' ']
    
    for line in data:
        if line[1]=='0': # Identifies the NRM line
            info_site[5]=line[2]
            nrm_data_out=info_site.copy()
    for line in data:            
        if line[0]=='C': # Identifies the component line
            comp_data=info_site.copy()
            comp_data.extend(line[1:12])
            comp_data_out.append(comp_data)
            # print('comp_data_out: ', comp_data_out)
    
    return nrm_data_out, comp_data_out


# Get the path where the script is located
base_path = os.path.dirname(os.path.abspath(__file__))

files_by_folder = get_rs3_files(base_path)

save_rs3_info(base_path, files_by_folder)