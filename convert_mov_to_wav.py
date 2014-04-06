#!/usr/bin/env python
# -*- coding: utf-8 -*-

## This script creates a Bash script to convert all MOV files in the current working directory into WAV files.

## Make sure you have nothing in the directory except this Python file and the MOV files.

import os
import subprocess

directory = os.listdir(os.getcwd())
for f in directory:
    if f[-4:] == '.mov':
        subprocess.call(['ffmpeg', '-i', f, f[:-4]+'.wav'])
