#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Wed Nov 16 15:47:10 2016

@author: QuentinDrillon
"""

import mne
import numpy as np
import pandas as pd
import lecture_fichier as lf

def print_list_files(fichier):
    list_all_files = lf.read_info(fichier)
    if '.DS_Store' in list_all_files:
        list_all_files.remove('.DS_Store')
    list_files = []
    list_seizures = lf.read_info_seizures(fichier)
    compteur = 0 
    for i in range(len(list_all_files)):
        if (compteur < len(list_seizures)) and (list_all_files[i][0] == list_seizures[compteur][0]) : 
                list_files.append(list_all_files[i][0])
                compteur += 1
    print('List of files to convert to csv :' + str(list_files))
    return list_files,list_seizures

def slashing_raw_file_into_10_min_DF(filepath,list_seizures):
    file = filepath.split('/')[-1]
    #on se place à la bonne seizure
    index = 0 
    while (file != list_seizures[index][0]): 
        index += 1
    
    # finding name and path of previous file 
    text = file.split('_')
    npatient = text[0].split('b')[1]
    text = text[1].split('.')[0]
    if (len(text.split('+')) > 1):
        nmoinsun = text.split('+')[0]
    else : 
        nmoinsun = int(text) - 1
        nmoinsun = str(nmoinsun)
        
    if (int(nmoinsun) < 10):
        newfile = ''.join(["chb",npatient,"_","0",nmoinsun,".edf"])
    else :
        newfile = ''.join(["chb",npatient,"_",nmoinsun,".edf"])
    newpath = ''.join(["data/chb",npatient,"/",newfile])
    if (int(nmoinsun) == 0):
        slashing_into_csv(filepath,'', index,3600000)
    elif (index == 0):
         print('Creating csv corresponding to first seizure ' + text)
         slashing_into_csv(filepath, newpath, index,3600000)
    elif (newfile == list_seizures[index-1][0]):
        to_previous_seizure = list_seizures[index][3] + (list_seizures[index-1][2] - list_seizures[index-1][1] - list_seizures[index-1][4])
        print('to_previous_seizure {}'.format(to_previous_seizure))
        if to_previous_seizure < 2400000:
            print('Seizure too close with previous one (< 45 minutes), must skip seizure ')
        elif to_previous_seizure < 4000000:
            print(('Creating csv corresponding to 30 minutes before seizure occuring during recording {} (1h15min > last seizure > 45 minutes)').format(text) )
            slashing_into_csv(filepath, newpath, index,1800000)
        else : 
            print(('Creating csv corresponding to 60 minutes before seizure occuring during recording {} (last seizure is close but not close enough to be a problem)').format(text))
            slashing_into_csv(filepath, newpath, index,3600000)
    else : 
        print('Creating csv corresponding to 60 minutes before seizure occuring during recording ' + text)
        slashing_into_csv(filepath, newpath, index,3600000)
    
def slashing_into_csv(filepath, newpath,index,duration):
    # Loading Data in actual file
    path = filepath
    raw_data = mne.io.read_raw_edf(path)
    dataframe = raw_data.to_data_frame()
    duration_sig = duration
    nb_df_to_create = duration_sig // 600000
    list_of_df = []
    numberd_in_actual_file = min(list_seizures[index][3] // 600000,nb_df_to_create) #combien de dataframe à créer dans le patient à la crise
    
    if (newpath == '') : #cas où la crise est dans le premier fichier
        print('No previous file, it is not going to be 6x10 minutes files')
        #création des dataframe de 10 minutes dans le recording contenant la crise
        if(numberd_in_actual_file > 0):
            for i in range(numberd_in_actual_file): 
                print("Creating dataframe {} ...".format(nb_df_to_create - i))
                start_df = dataframe.index[0] + list_seizures[index][3] - (i+1)*600000
                end_df = dataframe.index[0] + list_seizures[index][3] - i*600000
                print("Between {}ms and {}ms".format(start_df,end_df))
                new_df = pd.DataFrame(dataframe.loc[start_df : end_df ,: ])
                new_df.to_csv(path_or_buf=filepath[:len(filepath)-4]+'_{}.csv'.format(nb_df_to_create - i))
                list_of_df.append(new_df)
        
        #creation du 1er dataframe de moins de 10 minutes
        print("Creating dataframe {} ...".format(nb_df_to_create - numberd_in_actual_file))
        start_df = dataframe.index[0]
        end_df = dataframe.index[0] + list_seizures[index][3] - numberd_in_actual_file*600000
        print("Between {}ms and {}ms".format(start_df,end_df))
        new_df = pd.DataFrame(dataframe.loc[start_df : end_df ,: ])
        new_df.to_csv(path_or_buf=filepath[:len(filepath)-4]+'_{}.csv'.format(nb_df_to_create - numberd_in_actual_file))
        list_of_df.append(new_df)
        return;
    
    compteur = 0;
    #création des dataframe de 10 minutes dans le recording contenant la crise
    for i in range(numberd_in_actual_file): 
        compteur += compteur
        print("Creating dataframe {} ...".format(nb_df_to_create - i))
        start_df = dataframe.index[0] + list_seizures[index][3] - (i+1)*600000
        end_df = dataframe.index[0] + list_seizures[index][3] - i*600000
        print("Between {}ms and {}ms".format(start_df,end_df))
        new_df = pd.DataFrame(dataframe.loc[start_df : end_df ,: ])
        new_df.to_csv(path_or_buf=filepath[:len(filepath)-4]+'_{}.csv'.format(nb_df_to_create - i))
        list_of_df.append(new_df)
        
    if (compteur < nb_df_to_create):
        #creation du 1er dataframe de moins de 10 minutes
        print("Creating dataframe {} ...".format(nb_df_to_create - numberd_in_actual_file) + ' Part 2')
        start_df = dataframe.index[0]
        end_df = dataframe.index[0] + list_seizures[index][3] - numberd_in_actual_file*600000
        print("Between {}ms and {}ms".format(start_df,end_df))
        already_copied = list_seizures[index][3] - numberd_in_actual_file*600000
        new_df_to_merge_part2 = pd.DataFrame(dataframe.loc[start_df : end_df ,: ])
    
    
    # loading data from previous file
    new_raw_data = mne.io.read_raw_edf(newpath)
    new_dataframe = new_raw_data.to_data_frame()
    nb_df_remaining = nb_df_to_create - numberd_in_actual_file - 1
    
    if (compteur < nb_df_to_create):
        #création du 2e dataframe de moins 10 minutes 
        print("Creating dataframe {} ...".format(nb_df_to_create - numberd_in_actual_file) + ' Part 1')
        start_df = new_dataframe.index[-1] - (600000 - already_copied)
        end_df = new_dataframe.index[-1]
        print("Between {}ms and {}ms".format(start_df,end_df))
        new_df_to_merge_part1 = pd.DataFrame(new_dataframe.loc[start_df : end_df ,: ])
        
    
        #fusion des deux csv incomplet (chevauchement sur les deux enregistrements)
        print("Merging the two half dataframes : Creating dataframe {}".format(nb_df_to_create - numberd_in_actual_file))
        new_merged_df = new_df_to_merge_part1.append(new_df_to_merge_part2)
        new_merged_df.to_csv(path_or_buf=filepath[:len(filepath)-4]+'_{}.csv'.format(nb_df_to_create - numberd_in_actual_file))
        list_of_df.append(new_merged_df)
    
    if (nb_df_remaining > 0):
        #rest of the csvs
        for i in range(nb_df_remaining):
            print("Creating dataframe {} ...".format(nb_df_remaining - i))
            start_df = new_dataframe.index[-1] - (600000 - already_copied) - (i+1)*600000
            end_df = new_dataframe.index[-1] - (600000 - already_copied) - i*600000
            print("Between {}ms and {}ms".format(start_df,end_df))
            new_df = pd.DataFrame(new_dataframe.loc[start_df : end_df ,: ])
            new_df.to_csv(path_or_buf=filepath[:len(filepath)-4]+'_{}.csv'.format(nb_df_remaining - i))
            list_of_df.append(new_df)
        
        
    print(("All {} dataframes created").format(nb_df_to_create))

list_files,list_seizures = print_list_files('data/chb04/chb04-summary.txt')
for file in list_files:
    print(file)
    slashing_raw_file_into_10_min_DF('data/chb04/' + file,list_seizures)
