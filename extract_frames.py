#!/usr/bin/env python
# -*- coding: utf-8 -*-

## This script reads from TextGrid files produced in Praat the timestamps and labels of any annotations.
## It then extracts appropriately-named JPGs from those time points in the video file.

import sys
import re
import datetime
import subprocess


## CONSTANTS:
## (change these with each run)
C = 'LB' # C for consultant; change depending on whose files you're looking at.
SECTIONS = [3, 4, 5, 8] # change according to which numbered sections are available for each consultant; the video files should be labeled "(consultant's initials)(section number).mov", e.g. "LB3.mov"



def counting(vowels_so_far, tuple):
    """Return a three-digit number determined by how many tokens of a particular vowel have been previously identified: 004, 023, etc. (as EdgeTrak prefers).
    """
    if len(str(vowels_so_far.count(tuple[1])+1)) == 1:
        return '00'+str(vowels_so_far.count(tuple[1])+1)
    elif len(str(vowels_so_far.count(tuple[1])+1)) == 2:
        return '0'+str(vowels_so_far.count(tuple[1])+1)
    elif len(str(vowels_so_far.count(tuple[1])+1)) == 3:
        return str(vowels_so_far.count(tuple[1])+1)

def extract_section_frames(s, vowels_so_far):
    tg = open(C+str(s)+'.TextGrid', 'r').read()
    raw_times = re.findall("number = \d+\.\d\d\d", tg)
    times = []
    for item in raw_times:
        times.append(item[9:])
    raw_vowels = re.findall('mark = ".+"', tg)
    vowels = []
    for item in raw_vowels:
        vowels.append(item[8:-1])
    tuples = zip(times, vowels)

    for t in tuples:
        timestamp = str(datetime.timedelta(seconds=float(t[0])))[:-3]
        subprocess.call(['ffmpeg', '-i', str(C)+str(s)+'.mov', '-ss', '0'+timestamp, '-vframes', '1', t[1]+'-'+counting(vowels_so_far, t)+'.jpg'])
        vowels_so_far.append(t[1])
    return vowels_so_far


if __name__ == '__main__':
    vowels_so_far = [] # set of all vowels encountered so far (for numbering)
    for s in SECTIONS:
        vowels_so_far = extract_section_frames(s, vowels_so_far)

