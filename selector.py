import subprocess
import sys
import re
import os.path

filename = sys.argv[1]
job_id = sys.argv[2]
if (not os.path.exists(str(filename + "_parsed.txt"))):
	os.system("python parser.py " + filename)

#regex = r"Job ID: (\d+\[*\d*\]*)"
j_id = ""
start = "Job ID:"
end = "========================================\n"

read = False
dict_value = []
jobs_dict = {}

with open("parsed_files/" + filename + "_parsed.txt", "r") as f:
	for line in f:
		if(end in line):
			read = False
			jobs_dict[j_id] = dict_value
			dict_value = []
		if(start in line):
			read = True
			j_id = line.split(" ")[2][:-1]
			# matches = re.finditer(regex, line)
			# for matchNum, match in enumerate(matches):
			# 	j_id = match.group(1)
			#dict_value.append(line)
		if(read):
			dict_value.append(line)

with open("JOB_ID_" + job_id + ".txt", "w") as f:
	for key, value in jobs_dict.iteritems():
		if (key == job_id):
			for el in value:
				f.write(el)
				print(str(el[:-1]))


