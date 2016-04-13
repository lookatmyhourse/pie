#! /bin/bash

<< END_TXT
As input this scipt take the number of highest steps, or 
the given step at which we want to collect the information 
form the *dis files.
After finding all the *.dis files in the desired step folder
the script changes the cwd to the exact folder, since we need 
to extract filenames from the *.dat file, generate the *.json
file at the directory. 

The last step wil be to collect all .json files and to merge
them to one DataFrame 

END_TXT


step_number=$1 

# find all *dis files 
find . -regextype posix-egrep -regex "(.*$step_number.*\.*.dis)"


