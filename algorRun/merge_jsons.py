import pandas as pa

"""
Takes all the json databases from each foder and merges them thogether
forming a unique database of the result. 

run first the shell scipt

	angle_dist_all.sh

which will generate all the json files in each folder separatelly. 
After this step using 

find . -regextype posix-egrep -regex '(.*step_25.*\.*json)' -exec cp '{}' . \;




"""


jsonlist=[i for i in os.listdir(os.getcwd()) if i.split('.')[-1]=='json']
