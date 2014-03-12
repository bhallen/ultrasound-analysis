#!/usr/bin/env python
# -*- coding: utf-8 -*-


## This script allows you to combine vowel *.txt files into sets of those files for giving to R.  It can produce either sets of full vowels
## or groups of subsets of some vowels--the latter is useful for preventing one vowel (the one with more frames) in a group from having
## too great an effect on the shape of that group's contour.

## Note that the selection of "groups" is what determines the label applied in the first column to all the items from each vowel in 
## that group.

## Typical use will be creating a set of full vowel groups (using "all" at the first prompt, one group for each vowel, and one vowel per group) for
## vowel-to-vowel comparisons, then creating full vowel groups of vowels which are split into oral and nasal subsets or somesuch,
## and then finally creating the groups of subsets for vowel group testing:
## e.g. if you want to compare all the ATR vowels versus all the RTR vowels, and the vowel with the fewest number of frames has
## 11 frames, then you'll tell the script to take 10 frames per vowel, create two groups (ATR and RTR), and put all the ATR vowels into the
## first and all the RTR vowels into the second; comparing the resulting ATR and RTR groups should give a sense of how ATR and RTR
## vowels differ overall.


import csv
import sys, os

def trim_vowel (file, nf): # this function reads in individual vowel data files, 
                          # removes row 1, groups them by 30s (i.e. by frames),
                          # and takes an evenly spaced subset of length nf
    lines = []
    vowel_data = csv.reader(open(file), delimiter=' ')  # be sure columns are separated by a comma!
    v_rows = []
    for row in vowel_data:
        v_rows.append(row)
    del v_rows[0] # get ride of the column names
    frames = []
    n_frames = len(v_rows) / 30
    i = 0 # adding a list to frames for each frame (number of frames = n_frames)
    while i < n_frames:
        frames.append([])
        i += 1
    fi = 0 # frames iterator
    pi = 0 # points iterator
    for row in v_rows:
        frames[fi].append(row)
        pi += 1
        if pi == 30:
            pi = 0
            fi += 1
    if nf == 'all':
        trimmed_frames = []
        for frame in frames:
            trimmed_frames.append(frame)
    else:
        nf = int(nf)
        m = len(frames) / nf +1 # the script will make a subset of the data by taking every m'th frame
        trimmed_frames = []
        if m == 1:
            sys.exit("Too few frames!")
        for fi in range(0, len(frames)-1, m):
            trimmed_frames.append(frames[fi])
        needed = nf - len(trimmed_frames)
        for fi in range(1, needed*m, m):
            #print(str(fi)+" is "+str(frames[fi]))
            trimmed_frames.append(frames[fi])
    for frame in trimmed_frames:
        for point in frame:
            lines.append(point)
    #lines.append(["","end of vowel"])
    return lines
    
    

def main():
    nf = raw_input('How many frames per vowel?  Enter "all" to make a full multi-vowel list. ') # number of frames
    output_name = raw_input('Enter the name of the output file you want to create (no file extension): ')
    groups = [] # this will hold the actual content
    group_names = [] # this just holds the names
    gni = 0 # group_names iterator
    group_names.append(raw_input('Enter the name of the first group (e.g. FD-ATR-all): '))
    groups.append([])
    while group_names[gni] != 'end': # adds as many groups as needed (but it should generally be just 2 for the SSANOVA script...)
        gni += 1
        group_names.append(raw_input('Enter the name of the next group (e.g. FD-RTR-all); enter "end" if there are no more groups: '))
        groups.append([])
    group_names.pop(-1) # get rid of "end"
    groups.pop(-1) # get rid of the blank one
    print 'Groups: '+str(group_names)
    line_strings = [] # this will hold the lines converted from lists to strings
    for group in group_names: # adds each vowel to the group
        lines = [] # lines just in this group
        print 'Now ready to add to group "'+group+'".'
        v_choices = [] # which vowels are to be added to the group
        vci = 0 # v_choices iterator
        v_choices.append(raw_input('Enter the name of the first vowel in this group (e.g. FD-ATRe): '))
        while v_choices[vci] != 'end':
            vci += 1
            v_choices.append(raw_input('Enter the name of the next vowel in this group (e.g. FD-ATRi); enter "end" if there are no more vowels in this group: '))
        v_choices.pop(-1) # again, to get rid of "end"
        print 'Vowels in '+group+': '+str(v_choices)
        for vowel in v_choices: # call trim_vowel() to take subsets so that 1) R can handle the size; and 2) vowels have equal weight within the group
            for line in trim_vowel(vowel+'.txt', nf):
                lines.append(line)
        for line in lines: # fill in first column with the group name
            line[0] = group
        for line in lines: # we need strings to write properly to the .txt file, so...
            line_strings.append(' '.join(line))
    output_file = open(output_name+'.txt', 'w')
    output_file.write('word token X Y\n') # first line is added back so the R script works
    for line in line_strings:
        output_file.write(line+'\n')
        

# now the script creates a ready-made chunk of R script that should access the *.txt files just created and compare the first and last groups in it.  Primarily useful if you create a file with just two groups, which most of the outputs from Autogrouper.py (the actual groups) will be.

    output_r = open('R_'+output_name+'.txt', 'w') # now creating a second output file: the copy-pasteable chunk of R script to compare the groups
    r_text = '''
if(Sys.getenv("OS") != "")
{
	my.Filters = matrix(c("TXT files (*.TXT)","All files (*.*)","*.TXT","*.*"),2,2);
	input.traces = choose.files(caption="Select .txt files (multiple selection allowed)",filters=my.Filters);
} else 
{
	input.traces = \''''+os.getcwd()+'/'+output_name+'.txt\''''';
}

# The working directory is set to the folder that contains the TXT files by finding 
# the last "\\" and selecting a substring that stops there. 
not.found = TRUE;
search.index = nchar(input.traces[1]);
while(not.found && search.index >= 1){
	if(substring(input.traces[1],search.index,search.index)=="\\\\" | substring(input.traces[1],search.index,search.index)=="/"){
		not.found = FALSE;
	}else{
		search.index = search.index-1;
	}
}
my.Default = substring(input.traces[1],1,search.index);
setwd(my.Default);

# Filenames without the path are listed in the vector "input.traces.filenames".
input.traces.filename = substring(input.traces,search.index+1,nchar(input.traces))


# Read in the data

mydata = read.table(input.traces.filename,h=T,quote="\\"",dec=".", fill = TRUE, comment.char="")
mydata <- as.data.frame(mydata)

# Enter the labels for the three things you want to compare
#compare(mydata,"B2","B3", "B4", "B5")

compare(mydata, "'''+group_names[0]+'", "'+group_names[1]+'", "'+group_names[0]+'", "'+group_names[1]+'")'
    output_r.write(r_text)

if __name__ == '__main__':
    main()
    print("Grouping complete.")
    raw_input()

