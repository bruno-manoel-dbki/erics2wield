#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 17:41:27 2022

@author: bmdbki
"""

import os
import pandas as pd
from datetime import datetime

begin = datetime.now()
permutation = "3_1"
print("Running for "+permutation)
log = "log" + permutation


with open(log, 'a') as file:

    file.write('\nStarting in: ' + str(begin) + "\n")

#os.chdir("~/Documents/wield++/")
all_gb = pd.read_csv("Al_GBs_2022_HomerHart_Mendeley-4ykjz4ngwt.csv")

df = pd.DataFrame(  data = all_gb)
       
#df.head()



input_model = open("input.in", "r")

content = input_model.readlines()



axis_pos = {}


for i,x in enumerate(content):
    if "$AxisX1" in x :
        axis_pos["$AxisX1"] = i
    elif "$AxisZ1" in x: 
        axis_pos["$AxisZ1"] = i
    elif "$AxisX2" in x:
        axis_pos["$AxisX2"] = i
    elif "$AxisZ2" in x:
        axis_pos["$AxisZ2"] = i


#%%
# One output.ref - Reading and attach in the df in wield column

wield_energy = []
df_s3 = df#.head(10)

for index, row in df_s3.iterrows():
    file_id = row["planeID"]

    # permuatation select which vector from dataset we will select
    # it is defined in the beginning of the code to refer to log file

    if "1_2" in permutation:
        x1 = row[["A11","A12","A13"]]
        z1 = row[["A21","A22","A23"]]
        x2 = row[["B11","B12","B13"]]
        z2 = row[["B21","B22","B23"]]
    #    print ("Running for 1-2")
    
    elif "1_3" in permutation:
        x1 = row[["A11","A12","A13"]]
        z1 = row[["A31","A32","A33"]]
        x2 = row[["B11","B12","B13"]]
        z2 = row[["B31","B32","B33"]]
    #    print ("Running for 1-3")

    elif "2_3" in permutation:
        x1 = row[["A21","A22","A23"]]
        z1 = row[["A31","A32","A33"]]
        x2 = row[["B21","B22","B23"]]
        z2 = row[["B31","B32","B33"]]
    #    print ("Running for 2-3")
    
    elif "3_2" in permutation:
        x1 = row[["A31","A32","A33"]]
        z1 = row[["A21","A22","A23"]]
        x2 = row[["B31","B32","B33"]]
        z2 = row[["B21","B22","B23"]]
    #    print ("Running for 3-2")
    elif "3_1" in permutation:
        x1 = row[["A31","A32","A33"]]
        z1 = row[["A11","A12","A13"]]
        x2 = row[["B31","B32","B33"]]
        z2 = row[["B11","B12","B13"]]
    #    print ("Running for 3-1")

    elif "2_1" in permutation:
        x1 = row[["A21","A22","A23"]]
        z1 = row[["A11","A12","A13"]]
        x2 = row[["B21","B22","B23"]]
        z2 = row[["B11","B12","B13"]]
    #    print ("Running for 2-1")
    
    x1_s = '$AxisX1 ' + str(x1.values[0]) + " " + str(x1.values[1]) + " " + str(x1.values[2]) + "\n"
    z1_s = '$AxisZ1 ' + str(z1.values[0]) + " " + str(z1.values[1]) + " " + str(z1.values[2]) + "\n"
    x2_s = '$AxisX2 ' + str(x2.values[0]) + " " + str(x2.values[1]) + " " + str(x2.values[2]) + "\n"
    z2_s = '$AxisZ2 ' + str(z2.values[0]) + " " + str(z2.values[1]) + " " + str(z2.values[2]) + "\n"
    
    content[axis_pos["$AxisX1"]] = x1_s
    content[axis_pos["$AxisZ1"]] = z1_s
    content[axis_pos["$AxisX2"]] = x2_s
    content[axis_pos["$AxisZ2"]] = z2_s
    

    if( not os.path.exists(file_id)):
        print("Creating folder")
        os.mkdir(file_id)
       
    textfile = open(file_id + "/input.in", "w")
    for element in content:
        textfile.write(element)
    textfile.close()

    #Next block paste
    #os.chdir(file_id)
    print("Running Wield for " + file_id)
    try:
        os.system("./../wield/bin/wield " + file_id+ "/input.in -n 12")
        output = open("output.ref", "r")
        file_data =  output.readline().strip()
        energy = file_data.split(" ")[1]
        wield_energy.append([file_id, energy])
    except:
        energy = None
        wield_energy.append([file_id, energy])

    
    

    
    
    output.close()
    
    with open(log, 'a') as file:
        file.write(str(datetime.now() - begin) + " --> "+ str(index+1) + "/" + str(df.shape[0])+ " \n\t" + "ID: " + file_id + "\n\tEnergy: " + str(energy) + "\n")

df_wield = df_s3.copy()    
df_wield.insert(43,str("wieldEnergy" + permutation), None)

for each in wield_energy:
    df_wield.loc[df_wield["planeID"] == each[0],str("wieldEnergy" +permutation)] = each[1]


df_wield.to_csv("dataset_wield"+ permutation + ".csv")

  
input_model.close()

#%%




