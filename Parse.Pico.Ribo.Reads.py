#!/usr/bin/env python
'''
Parse PicoGreen/RiboGreen results from from Gemini XPS Microplate Reader
Convert 384 well plate format to 96 well plate format
Write to different excel spreadsheets

example:
python Parse.Pico.Ribo.Reads.py -f data/pico.reads.txt -s data/standards.txt -a1 1st_plate -a2 2nd_plate -b1 3rd_plate -b2 4th_plate
'''

from __future__ import print_function
import re
import argparse
import pandas as pd
from numpy import array
from numpy.random import rand, randn
import statsmodels.formula.api as sm
import matplotlib.pyplot as plt

#############
### functions
#############
def parse_matrix_of_data_from_plate(df, letters, numbers):
    ''' obtain matrix of data from 384 plate
	letters are row IDs
	numbers are column IDs
    '''
    matrix = []
    for letter in letters:
        row = []
        for number in numbers:
            row.append(df[number][letter])
        matrix.append(row)
    df2 = pd.DataFrame(array(matrix),index = abcdefgh, columns = n_1_to_12)
    return(df2)

def writeToExcel(df, sheet_name):
    ''' write data frame to excel spread sheets '''
    df.to_excel(writer, sheet_name=sheet_name, startrow=0 , startcol=0)
    df_stack = df.stack()
    df_stack_multipleindex = df_stack.reset_index()
    new_index = [ df_stack_multipleindex["level_0"][i] + str(df_stack_multipleindex["level_1"][i])  for i in range(len(df_stack_multipleindex["level_0"])) ]
    df_stack_singleindex = pd.DataFrame(df_stack.as_matrix(), index = new_index, columns = ["reads"])
    df_stack_singleindex.to_excel(writer, sheet_name= sheet_name, startrow=0 , startcol=15)


############################
### obtain args from command
############################
parser = argparse.ArgumentParser(description='please provide filename for Pico/Ribo reads')
parser.add_argument('-f', '--filename_result', type=str)
parser.add_argument('-s', '--filename_standard', type=str) # filename of Pico/Ribo standard

# four possible positions in the upper left corner of a 384 well plate
"""
 a1 | a2
---- ----
 b1 | b2
"""
parser.add_argument('-a1', '--a1_plate_name', type=str)
parser.add_argument('-a2', '--a2_plate_name', type=str)
parser.add_argument('-b1', '--b1_plate_name', type=str)
parser.add_argument('-b2', '--b2_plate_name', type=str)

args = parser.parse_args()
filename_result = args.filename_result
filename_standard = args.filename_standard
a1_plate_name = args.a1_plate_name
a2_plate_name = args.a2_plate_name
b1_plate_name = args.b1_plate_name
b2_plate_name = args.b2_plate_name


#######################################################################
### define row IDs and column IDs of plates (both 384 well and 96 well)
####################################################################### 
# define row IDs (letters)
a_to_p = [chr(i) for i in range(ord('a'),ord('p')+1)]
acegikmo = a_to_p[::2]
bdfhjlnp = a_to_p[1::2]
abcdefgh = a_to_p[:8]

# define column IDs (numbers)
n_1_to_24 = list(range(1,25))
n_odd = list(map(int,n_1_to_24[::2]))
n_even = list(map(int, n_1_to_24[1::2]))
n_1_to_12 = list(range(1,13))


#################################
### fetch data of Pico/Ribo reads
#################################
''' fetch Pico/Ribo reads of whole samples '''
wholeMatrix = []
for line in open(filename_result,"r"):
    lst = line.rstrip().lstrip().split("\t")
    if len(lst) == 24:
        wholeMatrix.append(list(map(float,lst)))

df = pd.DataFrame(array(wholeMatrix),index = a_to_p, columns = n_1_to_24)


#####################################
### fetch data of Pico/Ribo standards
#####################################
''' get well IDs and corresponding concentrations'''
standardDict = {}
for line in open(filename_standard,"r"):
    if line.startswith(tuple(a_to_p)): # if startswith well ID
        lst = line.rstrip().split("\t")
        standardDict[lst[0]] = lst[1]

''' fetch Pico/Ribo reads of standards '''
standardMatrix = []        		
for well in sorted(standardDict):
    letter, number = well[:1], well[1:]
    concentration = standardDict[well]
    reads = df[int(number)][letter]
    standardMatrix.append([float(reads),float(concentration)])

df_std = pd.DataFrame(array(standardMatrix),columns = ["reads","concentration(ng/ul)"]).sort("concentration(ng/ul)")

##############################################
### parse data and write to excel spreadsheets
##############################################
writer = pd.ExcelWriter(filename_result.replace("txt", "xlsx"), engine='xlsxwriter')

''' raw data in 384 well format '''
df.to_excel(writer, sheet_name='raw')

''' reads of Pico/Ribo standards and their known concentration (ng/ul) '''
df_std.to_excel(writer, sheet_name='standard')

''' write 96 well format for each position (if data is available)
 a1 | a2
---- ----
 b1 | b2
'''
if a1_plate_name:
    a1_df = parse_matrix_of_data_from_plate(df, acegikmo, n_odd)
    writeToExcel(a1_df, a1_plate_name)

if b1_plate_name:
    b1_df = parse_matrix_of_data_from_plate(df, bdfhjlnp, n_odd)
    writeToExcel(b1_df, b1_plate_name)

if a2_plate_name:
    a2_df = parse_matrix_of_data_from_plate(df, acegikmo, n_even)
    writeToExcel(a2_df, a2_plate_name)
	
if b2_plate_name:
    b2_df = parse_matrix_of_data_from_plate(df, bdfhjlnp, n_even)
    writeToExcel(b2_df, b2_plate_name)

writer.close()
