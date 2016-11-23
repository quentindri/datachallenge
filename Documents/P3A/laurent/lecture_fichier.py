#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 14:46:24 2016

@author: QuentinDrillon
"""
import numpy as np
import pandas as pd

def read_info_seizures(filepath):
    fichier = open(filepath,"r")
    ftr = [3600,60,1]
    files_name= []
    start_time = []
    end_time = []
    number_seizures =[]
    start_time_seizures = []
    end_time_seizures = []
    
    for line in fichier:
        if line.find("File Name") >= 0 : # file name
            text = line.split(' ')
            text = text[2].split('\n')
            files_name.append(text[0])
        if line.find("File Start Time") >= 0 : #horaires de début d'enregistrement
            text = line.split(' ')
            text = text[3].split('\n')
            start_time.append(text[0])
        if line.find("File End Time") >= 0 : #horaires de fin d'enregistrement 
            text = line.split(' ')
            text = text[3].split('\n')
            end_time.append(text[0])
        if line.find("Seizures in File") >= 0 : #enregistrement contient une seizure
            text = line.split(' ')
            text = text[5].split('\n')
            number_seizures.append(text[0]) 
        if line.find("Seizure Start Time") >= 0 : #début des seizures
            text = line.split(' ')
            start_time_seizures.append(text[3])
        if line.find("Seizure End Time") >= 0 : # fin des seizures
            text = line.split(' ')
            end_time_seizures.append(text[3])
        
    number_crises = 0
    start_time_withcrisis = []
    end_time_withcrisis = []
    file_name_withcrisis = []
    for i in range(len(number_seizures)):
        if(number_seizures[i] == '1'): 
            number_crises += 1 #on compte le nombre de crises 
            file_name_withcrisis.append(files_name[i])
            start_time_withcrisis.append(start_time[i]) #on ne garde que les enregistrements
            end_time_withcrisis.append(end_time[i]) #avec des crises
    
    recorded_seizures = [] #tableau contenant les horaires de début et de fin de chaque crise 
    #[début1,fin1,...,débutn,fin,]
    
    for i in range(number_crises):
        recorded_seizures.append([])
    
    for i in range(len(start_time_withcrisis)):
        start_time_withcrisis[i] = 1000*sum([a*b for a,b in zip(ftr, map(int,start_time_withcrisis[i].split(':')))])
        end_time_withcrisis[i] = 1000*sum([a*b for a,b in zip(ftr, map(int,end_time_withcrisis[i].split(':')))])
        start_time_seizures[i] = 1000*int(start_time_seizures[i])
        end_time_seizures[i] = 1000*int(end_time_seizures[i])

        
    for i in range(number_crises):
        recorded_seizures[i].append(file_name_withcrisis[i])
        recorded_seizures[i].append(start_time_withcrisis[i])
        recorded_seizures[i].append(end_time_withcrisis[i])
        recorded_seizures[i].append(start_time_seizures[i])
        recorded_seizures[i].append(end_time_seizures[i])
    
    return(recorded_seizures)
    
def read_info(filepath):
    fichier = open(filepath,"r")
    ftr = [3600,60,1]
    files_name= []
    start_time = []
    end_time = []
    
    for line in fichier:
        if line.find("File Name") >= 0 : # file name
            text = line.split(' ')
            text = text[2].split('\n')
            files_name.append(text[0])
        if line.find("File Start Time") >= 0 : #horaires de début d'enregistrement
            text = line.split(' ')
            text = text[3].split('\n')
            start_time.append(text[0])
        if line.find("File End Time") >= 0 : #horaires de fin d'enregistrement 
            text = line.split(' ')
            text = text[3].split('\n')
            end_time.append(text[0])
    recording_list = []

    for i in range(len(start_time)):
        recording_list.append([])
    
    for i in range(len(start_time)):
        start_time[i] = 1000*sum([a*b for a,b in zip(ftr, map(int,start_time[i].split(':')))])
        end_time[i] = 1000*sum([a*b for a,b in zip(ftr, map(int,end_time[i].split(':')))])
        
    for i in range(len(start_time)):
        recording_list[i].append(files_name[i])
        recording_list[i].append(start_time[i])
        recording_list[i].append(end_time[i])
    
    return(recording_list)
    
read_info_seizures('data/chb03/chb03-summary.txt')