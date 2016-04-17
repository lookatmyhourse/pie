import pandas as pa

"""
Takes all the json datasets from each foder and merges them thogether
forming a unique database of the result. 

run first the shell scipt with similar argument: 

	angle_dist_all.sh step_25

which will generate all the json files in each folder separatelly. 
The shell script will also copy all the json files to the 'mother 
folder'. 

"""

# make a list of all json file found in the 'mother folder'
jsonlist=[i for i in os.listdir(os.getcwd()) if i.split('.')[-1]=='json']

df_sum=pa.DataFrame()
for i in jsonlist:
	df_sum=pa.concat([df_sum,pa.read_json(i)])

		
