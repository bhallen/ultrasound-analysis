#!/usr/bin/env python
# -*- coding: utf-8 -*-

## The *.con files that EdgeTrak produces are not in a format that can be used by SSANOVA_functions_plot.R .  This script converts the *.con files into *.txt files in a usable format.

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

    print len(x_coords)
    print len(y_coords)
    new_rows = []
    i = 0
    while i < len(x_coords):
        row = []
        row.append(x_coords[i])
        row.append(y_coords[i])
        new_rows.append(row)
        i += 1
    
    print len(new_rows)
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
    for row in new_rows:  # but we need to make the lists into strings for writing to file
        row_str = ' '.join(row)  # produces space-delimited *.txt files
        row_str += '\n'
        final_rows.append(row_str)
    print final_rows
    return final_rows  # this is the list of strings
        
            


def main():
    cwd = os.getcwd()
    for file in os.listdir(cwd):
        if ".con" in file:
            converted = tidy_up (file)
            print str(file)
            name = str(file)[0:-4]
            file = open(name+".txt", "w")
            file.writelines(converted)

if __name__ == '__main__':
    main()

