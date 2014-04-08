#!/usr/bin/env python
# -*- coding: utf-8 -*-


## This script allows you to combine segment *.txt files, such as those from edgetrak_output_converter.py.  Given a set of *.txt files each with data from an individual segment, this script groups them into whatever two groups you wish to compare using the R script.

## Example 1: comparing two segments
## In this case, both groups consist of only one segment apiece.  Say you want to compare FD's [e] to their [o], and these data are stored in FD-e.txt and FD-o.txt, respectively.  Run the script, and at the first prompt, enter 'all' (without quotes) and press Enter/Return.  (Using 'all' here means that there is no limit set on how many tokens are used from each vowel.)  At the next prompt, enter the name of the file you want the script to output, e.g. 'FD-e-vs-o' (do not enter a file extension).  When prompted for the name of the first group, enter 'mid-front', and when asked for the name of the next group, enter 'mid-back'.  Since there are only two groups of interest for now, enter 'end' at the next prompt.  Now you will add component segment files into the groups.  Since the one vowel in the 'mid-front' group is [e], stored in the file FD-e.txt, you will enter 'FD-e' at the next prompt.  Enter 'end' at the following one to end addition of vowels into this group.  When prompted to add a vowel to the 'mid-back' group, enter 'FD-o', then end at the next prompt.  The output file will now be created.

## Example 2: comparing two groups of segments
## Suppose that you want to compare the two high vowels [u] and [i] as a group (average) to the two mid vowels [o] and [e], in order to determine whether there are any articulatory differences between the two classes.  Now suppose that you have 20 tokens of [u], [i], and [o], but only 15 tokens of [e].  In order to ensure that the data from [o] is not overrepresented in the mid vowel group ([o] and [e]), you must limit the number of tokens to 15.  In such a scenario, at the first prompt ('frames per segment'), you will enter '15'.  Then continue to create the two groups ('high' and 'mid') and add vowels to each group normally (add 'FD-u', and 'FD-i' to 'high', then add 'FD-e' and 'FD-o' to mid, assuming the same file name convention as Example 1).

## Example 3: creating a file with all vowel groups
## The files that this script creates are not limited to having only two groups.  You may wish to create a single file with all data from every segment group of interest, and then pick out subsets of it to compare using the R script.  This can be done in the same way as the examples above: simply continue adding more groups after the second one.  You are free to include a particular vowel's data in multiple groups.

## Note that the selection of "groups" is what determines the label applied in the first column to all the items from each segment in that group.

## Typical use will involve creating a set of full segment groups (using "all" at the first prompt, one group for each segment, and one segment per group) for segment-to-segment comparisons, then creating full segment groups of segments which are split into, e.g. oral and nasal subsets, and then finally creating the groups of subsets for segment group testing.




import csv
import sys, os

def trim_segment (file, nf):
    """Read in individual segment data files, 
    remove row 1, group them by 30s (i.e. by frames),
    and takes an evenly spaced subset of length nf.
    """
    lines = []
    segment_data = csv.reader(open(file), delimiter=' ')  # be sure columns are separated by a comma!
    v_rows = []
    for row in segment_data:
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
    #lines.append(["","end of segment"])
    return lines
    
    

def main():
    nf = raw_input('How many frames per segment?  Enter "all" to make a full multi-segment list. ') # number of frames
    output_name = raw_input('Enter the name of the output file you want to create (no file extension): ')
    groups, group_names = [], []
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
    for group in group_names: # adds each segment to the group
        lines = [] # lines just in this group
        print 'Now ready to add to group "'+group+'".'
        v_choices = [] # which segments are to be added to the group
        vci = 0 # v_choices iterator
        v_choices.append(raw_input('Enter the name of the first segment in this group (e.g. FD-ATRe): '))
        while v_choices[vci] != 'end':
            vci += 1
            v_choices.append(raw_input('Enter the name of the next segment in this group (e.g. FD-ATRi); enter "end" if there are no more segments in this group: '))
        v_choices.pop(-1) # again, to get rid of "end"
        print 'segments in '+group+': '+str(v_choices)
        for segment in v_choices: # call trim_segment() to take subsets so that 1) R can handle the size; and 2) segments have equal weight within the group
            for line in trim_segment(segment+'.txt', nf):
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

