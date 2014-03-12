#!/usr/bin/env python
# -*- coding: utf-8 -*-

## This script creates a Bash script to convert all video files in the current working directory into WAV files.

## Make sure you have nothing in the directory except this Python file and the MOV files.

import os

def main():

    output = []

    directory = os.listdir(os.getcwd())
    for file in directory:
        if file[-4:] == '.mov':
            output.append('ffmpeg -i '+file+' '+file[:-4]+'.wav\n')
    FILE = open('mov_convert.sh', 'w')
    FILE.write('#!/bin/sh\n\n')
    FILE.writelines(output)
    print('mov_convert.sh has been created.')
if __name__ == '__main__':
    main()

