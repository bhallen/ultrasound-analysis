#!/usr/bin/env python
# -*- coding: utf-8 -*-

## This script creates a Bash script to convert all MOV files (files with the .mov extension only) in the current working directory into WAV files.

## If running this script from a terminal window, please ensure that your current working directory is the one containing the .mov files.  In case you encounter problems, make sure you have nothing in the directory except this Python file and the MOV files.

import os
import subprocess

directory = os.listdir(os.getcwd())
for f in directory:
    if f[-4:] == '.mov':
        subprocess.call(['ffmpeg', '-i', f, f[:-4]+'.wav'])
