ultrasound-analysis
===================

A package of scripts for processing and analysis of ultrasound data for research in linguistics

### DESCRIPTION ###

The scripts in this directory (make_move_convert.py, make_frame_extraction.py, edgetrak_output_converter.py, and autogrouper.py) automate four otherwise tedious parts of the process of extracting data from ultrasound movies or any other annotated video file.

Using these scripts requires that you have installed Python 2.7 ( http://www.python.org/getit/ ) as well as Bash ( http://en.wikipedia.org/wiki/Bash_(Unix_shell) ).  Python can be installed as offered on python.org; Bash should come installed on most Linux and Mac OS X systems, and you can use Cygwin ( http://www.cygwin.com/ ) if you are on Windows.  FFmpeg ( http://ffmpeg.org/ ) is also required---make sure that 'ffmpeg' is a command available in your terminal environment.

These scripts are provided as-is.  Note that I am not affiliated with the makers of EdgeTrak, nor with Adam Baker or Joanna Brugman, who created the SSANOVA script for R that these scripts were designed to integrate with.

Blake H. Allen


(** ADD EdgeTrak download link to README **)


#### INSTRUCTIONS ####

1) Put make_move_convert.py in the same directory as the video files, which must be titled in the format "(two-character initials of informant)(1- or 2-digit number of section).mov".  E.g.: 'BA1.mov', 'XY23.mov'

2) Add execute permissions to make_move_convert.py and execute it.  This creates mov_convert.sh, which you may modify manually if necessary.

3) Add execute permissions to mov_convert.sh and execute it, producing a WAV file for each video file.

4) Now annotate the WAV files in Praat using a point tier.

5) Once the annotations are finished and saved as X.TextGrid (where X = the file name of the associated video, without its extension), put them in a directory along with the MOV files and make_frame_extraction.py.

6) Modify make_frame_extraction.py such that the "c" variable (line 13) is set to the initials of the relevant consultant, and also such that the "sections" list (line 14) contains the numbered sections you're having the script iterate over.  These are both toward the bottom of the file, within the definition of the main function.  NOTE: depending on your Praat version, you may need to change "number" on line 28 to "time", and the "9" on line 31 to "7" (to adjust for the different sizes of those two words).  

7) Add execute permissions to make_frame_extraction.py and execute it.  This creates frame_extraction.sh.

8) After making any manual modifications that you need, add execute permissions to frame_extraction.sh and execute it to produce JPG files from the annotated time points in each video, all titled in a format ready to be given to EdgeTrak.

9) Once you have created *.con files using EdgeTrak (see EdgeTrak documentation, and NOTE below), put all those *.con files in a directory along with edgetrak_output_converter.py and run it; it will produce vowel *.txt files which are now ready to be grouped together.  NOTE: The SSANOVA script requires that each contour consist of no more than 30 points.  You can set this in the "save .con file" dialog.  Also be sure that the number of points and scaling constant are the same for all contours across your entire data set.

10) Use autogrouper.py to produce a file containing all individual vowels (for comparison of individual vowels) and/or files containing groups of subsets of vowels.  Open up autogrouper.py in a text editor and read its comments for more help.

11) Once your group *.txt files are created, you can paste the chunk of R code that autogrouper.py creates into the proper place at the end of the SSANOVA_functions_plot.R script and run it to compare the first and last group (or--more likely in the cases this feature is designed for--the only two groups) of that *.txt file.  You can also use the SSANOVA_functions_plot.R script as is and then choose the group *.txt file through the file select utility that pops up, but you will need to add a line to the end of the R script specifying which two groups you want to compare, according to this template:
compare(mydata, "(first group/vowel)", "(second group/vowel)", "(label for first group/vowel)", "(label for second group/vowel)")
e.g.:
compare(mydata, "KA-ISP", "KA-ATR", "KA's ISP", "KA's ATR Vowels")


#### SUMMARY ####

MOV files -> make_move_convert.py -> mov_convert.sh -> Praat annotations -> TextGrids -> make_frame_extraction.py -> frame_extraction.sh -> JPGs -> EdgeTrak -> edgetrak_output_converter.py -> autogrouper.py -> R SSANOVA script -> result graphs

