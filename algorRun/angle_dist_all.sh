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

run the script at the _refinements folder 

END_TXT

# to path to the root folder 
starting_dir=`pwd`	

# a function for folder change 
# it takes an argument ! as:
# to_cd arch_3_1_127_1
#
to_cd(){ cd "$1"; }   # when writing a bash function this is equal to
to_cd(){
cd "$1"

angle_dist_.sh

cd $starting_dir
}



# the step number is forwarded to this script 
# by calling: 
# angle_dist_all.sh 26 
step_number=$1 

# find all *dis files for a certain step / step_folder
f=`find . -regextype posix-egrep -regex "(.*$step_number.*\.*.dis)"`



# navigate to the folder where the *.dis is 

# execute 'angle_dist_.sh' that will generate the json file for that refinemets *.dis

# get back to root folder 

# repeat for all subfolders and all *dis files 

# find all *.json files copy them to the root, open in python and merge them 









