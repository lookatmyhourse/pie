#! /bin/bash

#----------------------------------------------
#folder name
#cwd_name=`echo ${PWD##*/}`
#generate a filename from the folder name 
# this file will contain the redued lines of the 
# merged files of angle and distance 
#a_d_filename=`echo $cwd_name".txt"`
#----------------------------------------------

# better way would be to generate the filename from 
# the *.dat file, which is anyhow unique in te folder 
#datf=`find . -iname *.dat`
datf_b=`(basename $(find . -iname *.dat))`
a_d_filename=`echo "${datf_b/.dat}"`
echo $a_d_filename

# get the relation and the angle values 
a=`grep '(.*o[^0..9].*)-(.*p1.*)-(.*o[^0..9]' *.dis | awk '{print " "$2"-"$4"-"$6" "$8}' > angle.txt`

# get the distances 
d=`grep 'Atm-1.*Atm-2.*Atm-3' *.dis | awk '{print " "$6" "$9" "$12}' > distances.txt `

# merge the two files 'angles.txt' and 'distances.txt' line by line
`paste angle.txt distances.txt > ab.txt`

# remove dupliates but leave one of it, and save it to a file 
`awk '!x[$0]++' ab.txt > $a_d_filename`

# run the python code to extract relevant data 
# and to generate a json database 
python /bin/py_classes/angle_dist_.py $a_d_filename

# remove temporary files/ cleanup 
`rm angle.txt distances.txt ab.txt $a_d_filename`
