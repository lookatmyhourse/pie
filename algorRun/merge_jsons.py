import pandas as pa
import os
"""
Takes all the json datasets from each folder and merges them together
forming a unique database of the result. 

run first the shell script with similar argument: 

	angle_dist_all.sh step_25

which will generate all the json files in each folder separately. 
The shell script will also copy all the json files to the 'mother 
folder'. 

"""

# make a list of all json file found in the 'mother folder'
jsonlist=[i for i in os.listdir(os.getcwd()) if i.split('.')[-1]=='json']

df_sum=pa.DataFrame()
for i in jsonlist:
	df_sum=pa.concat([df_sum,pa.read_json(i)])

file_list_by_type=[f for f in os.listdir(".") if f.endswith(".json")]
[os.remove(i) for i in file_list_by_type]
df_sum.to_csv('df_sum.csv')

df=pa.read_csv('df_sum.csv')
df_sec=df[['o1-o2', u'o1-o3', u'o1-p1',u'o2-o3', u'o2-p1', u'o3-o3',u'o3-p1']]
pa.scatter_matrix(df_sec)




		
