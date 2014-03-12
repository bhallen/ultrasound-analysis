#!/usr/bin/env python
# -*- coding: utf-8 -*-

## This script reads from TextGrid files produced in Praat the timestamps and labels of any annotations.
## It then constructs a Bash script which extracts appropriately-named JPGs from those time points in video.

import sys
import re
import datetime


## CONSTANTS:
## (change these with each run)
c = 'HS' # c for consultant; change depending on whose files you're looking at.
sections = [1, 2, 4, 5, 8] # change according to which numbered sections are available for each consultant; the video files should be labeled "(consultant's initials)(section number).mov", e.g. "LB3.mov"


## returns a three-digit number determined by how many tokens of a particular vowel have been previously identified: 004, 023, etc. (as EdgeTrak prefers).
def counting (all_vowels, tuple):
    if len(str(all_vowels.count(tuple[1])+1)) == 1:
        return '00'+str(all_vowels.count(tuple[1])+1)
    elif len(str(all_vowels.count(tuple[1])+1)) == 2:
        return '0'+str(all_vowels.count(tuple[1])+1)
    elif len(str(all_vowels.count(tuple[1])+1)) == 3:
        return str(all_vowels.count(tuple[1])+1)

## tg_to_sh = TextGrid to Shell (script)
def tg_to_sh (s, c, f_out):
    ## 
    tg = open(c+str(s)+'.TextGrid', 'r').read()
    raw_times = re.findall("number = \d+\.\d\d\d", tg)
    times = []
    for item in raw_times:
        times.append(item[9:])
    raw_vowels = re.findall('mark = "\w+"', tg)
    vowels = []
    for item in raw_vowels:
        vowels.append(item[8:-1])
    tuples = zip(times, vowels)
    print(tuples)
    text = f_out[0] # text that will eventually be output as the shell script
    all_vowels = f_out[1]
    for t in tuples:
        timestamp = str(datetime.timedelta(seconds=float(t[0])))[:-3]
        text.append('ffmpeg -i '+str(c)+str(s)+'.mov -ss 0'+timestamp+' -vframes 1 '+t[1]+'-'+counting(all_vowels, t)+'.jpg\n')
        all_vowels.append(t[1])
    f_out = [text, all_vowels]
    return f_out
            
def main():
    f_out = [[],[]] # (function_output) list of two lists: first is the gradually-built body of the .sh file, and the second is the set of all vowels encountered so far (for numbering)
    all_vowels = []
    for s in sections:
        f_out = tg_to_sh(s, c, f_out)
    FILE = open('frame_extraction.sh', 'w')
    FILE.write('#!/bin/sh\n\n')
    FILE.writelines(f_out[0])
    print('frame_extraction.sh has been created.')

if __name__ == '__main__':
    main()

