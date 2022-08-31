# Wield and BYU dataset
 
This project works with [Wield](https://github.com/solidsgroup/wield) and use the dataset provided by the authors of [Examination of computed aluminum grain boundary structures and energies that span the 5D space of crystallographic character](https://www.sciencedirect.com/science/article/pii/S1359645422003871?via%3Dihub)
 
## Input

### Wield
The input.in contains the base configuration to run wield
 
### Dataset
To begin, you will need to ask the author of the article cited. Just insert the file in this repository. If it didn't work, check the file name in the code, if it is correct.
 

## Configuration
 
### Setting Wield
Clone wield repository, compile, and alias the command to your PATH
 
### Selecting Axis
In main.py you can choose the combination of axes you want to use. The options that was implemented are:
* 1_2
* 1_3
* 2_1
* 2_3
* 3_1
* 3_2
 
### Process steps files
A new folder will be created for each sample in the dataset. Folder names are equal to the respective Plane_ID in the dataset. This folder contains the input file necessary to run wield.
 
Also a file named output is created as a temp file. It contains the energy output from Wield. This file is used to feed the output dataset
 
## Output
 
After finish the process a file named dataset_wield_*permutation*.csv will be created.
 
 
## Log
A log file is created while you run the code. The name is based on the permutaion you selected when running the code
 
 

