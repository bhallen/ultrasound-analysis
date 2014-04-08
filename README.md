ultrasound-analysis
===================

A package of scripts for processing and analysis of ultrasound data for research in linguistics

### DESCRIPTION ###

The scripts in this directory (convert_mov_to_wav.py, extract_frames.py, convert_edgetrak_output.py, and autogrouper.py) automate four otherwise tedious parts of the process of extracting, processing, and analyzing data from ultrasound movies or any other annotated video file.

These scripts are provided as-is.  Note that I am not affiliated with the makers of EdgeTrak, nor with Adam Baker or Joanna Brugman, who created the SSANOVA script for R that these scripts were designed to integrate with.


### DEPENDENCIES ###

You must have these programs installed in order to use all of the scripts included here:
1. Python 2.7 --- http://www.python.org/getit/
2. FFmpeg --- http://ffmpeg.org/ .  Make sure that the 'ffmpeg' command is available in your terminal environment.
3. (See note below!) A terminal program, such as Bash.  This is generally pre-installed on Linux and Mac OS X as Terminal.  If you use Windows, I recommend that you use Cygwin --- http://www.cygwin.com/

Note that if you only want to use a subset of the scripts included here, you may not need all of the above programs.  Most notably, if you do not want to use autogrouper.py to prepare segment *.txt files for giving to the R script, you do not need access to a terminal environment.


### RELATED SOFTWARE ###

Parts of this package are designed for use with EdgeTrak, which allows you to extract contour information from ultrasound images.  You can download EdgeTrak here:
http://speech.umaryland.edu/software.html

Note that I am not affiliated with the makes of EdgeTrak.  Please refer to the citation below:
Li, M., Kambhamettu, C., and Stone, M. (2005) Automatic contour tracking in ultrasound images. Clinical Linguistics and Phonetics 19(6-7); 545-554.



### INSTRUCTIONS ###

*STEP 1*: Convert ultrasound movie files (in .mov format) to audio (.wav) files that you can use for making Praat TextGrids

1.1) Put convert_mov_to_wav.py in the same directory as the video files, which must be titled in the format "(two-character initials of informant)(1- or 2-digit number of section).mov".  E.g.: 'BA1.mov', 'XY23.mov'

1.2) Add execute permissions to convert_mov_to_wav.py and execute it.  To do so, you may either run the script from a terminal window using python, or simply double-click the file and choose to run it.


*STEP 2*: Annotate the WAV files in Praat using a point tier.


*STEP 3*: Extract still frames (images) from your ultrasound movie files using the TextGrid(s)

3.1) Once the annotations are finished and saved as X.TextGrid (where X = the file name of the associated video, without its extension), put them in a directory along with the MOV files and extract_frames.py.

3.2) Modify extract_frames.py in a text editor: set the "C" variable (line 15) to the initials of the relevant consultant, and also set the "sections" list (line 16) such that it contains the numbered sections you're having the script iterate over.

3.2*) NOTE: depending on your Praat version, you may need to change "number" on line 32 to "time", and the "9" on line 35 to "7" (to adjust for the different sizes of those two words).  This is due to differences in TextGrid formats between Praat versions. 

3.3) Add execute permissions to extract_frames.py and execute it.  This produces JPG files from the annotated time points in each video, all titled in a format ready to be given to EdgeTrak.


*STEP 4*: Import the JPG files into EdgeTrak and create .con files encoding the relevant contour data.
NOTE: The SSANOVA script requires that each contour consist of no more than 30 points.  You can set this in the "save .con file" dialog.  Also be sure that the number of points and scaling constant are the same for all contours across your entire data set.


*STEP 5*: Convert EdgeTrak outputs (.con files) into .txt files that can be used with the R script

5.1) Put all those *.con files in a directory along with convert_edgetrak_output.py and run it.  This will produce corresponding *.txt files.


*STEP 6*: Combine vowel data into groups of interest and give to the R script

6.1) Use autogrouper.py to produce a file containing all individual vowels (for comparison of individual vowels) and/or files containing groups of subsets of vowels.  Open up autogrouper.py in a text editor and read its comments for more help.

6.2) Once your group *.txt files are created, you can paste the chunk of R code that autogrouper.py creates into the proper place at the end of the SSANOVA_functions_plot.R script and run it to compare the first and last group (or---more likely in the cases this feature is designed for---the only two groups) of that *.txt file.  You can also use the SSANOVA_functions_plot.R script as is and then choose the group *.txt file through the file select utility that pops up, but you will need to add a line to the end of the R script specifying which two groups you want to compare, according to this template:
compare(mydata, "(first group/vowel)", "(second group/vowel)", "(label for first group/vowel)", "(label for second group/vowel)")
e.g.:
compare(mydata, "KA-ISP", "KA-ATR", "KA's ISP", "KA's ATR Vowels")


### SUMMARY ###

MOV files -> convert_mov_to_wav.py -> Praat annotations -> TextGrids -> extract_frames.py -> JPGs -> EdgeTrak -> convert_edgetrak_output.py -> autogrouper.py -> R SSANOVA script -> result graphs

