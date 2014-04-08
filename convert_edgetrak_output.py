#!/usr/bin/env python
# -*- coding: utf-8 -*-

## The *.con files that EdgeTrak produces are not in a format that can be used by SSANOVA_functions_plot.R.  This script converts the *.con files into *.txt files in a usable format.

## If running this script from a terminal window, please ensure that your current working directory is the one containing the .con files.

import csv
import sys
import os

def tidy_up (file):
    x_coords = []
    y_coords = []
    vowel_data = csv.reader(open(file), delimiter='\t')  # the *.con files are tab-delimited
    for row in vowel_data:
        i = 0
        while i < len(row):  # put the x and y coords together
            row[i] = row[i].lstrip()  # get rid of that space on the left
            if len(row[i]) > 0:
                if i % 2 == 0:
                    x_coords.append(row[i])
                else:
                    y_coords.append(row[i])
            i += 1

    new_rows = []
    i = 0
    while i < len(x_coords):
        row = []
        row.append(x_coords[i])
        row.append(y_coords[i])
        new_rows.append(row)
        i += 1
    
    i = 0
    j = 0
    for row in new_rows:
        if i % 30 == 0:
            j += 1
        row.insert(0, str(j))
        row.insert(0, str(i+1))
        i += 1
        
    c_names = ['word','token','X','Y']  # column names
    new_rows.insert(0, c_names)  # now new_rows has lists of rows
    
    final_rows = []
    for row in new_rows:
        row_str = ' '.join(row)  # produces space-delimited *.txt files
        row_str += '\n'
        final_rows.append(row_str)
        
            


def main():
    cwd = os.getcwd()
    for f in os.listdir(cwd):
        if ".con" in f:
            converted = tidy_up(f)
            name = str(f)[0:-4]
            with open(name+".txt", "w") as f:
                f.writelines(converted)

if __name__ == '__main__':
    main()

