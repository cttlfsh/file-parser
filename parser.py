from collections import Counter
import re 
import datetime
import sys

filename = sys.argv[1]

def individuate_match(regexp):
	regexp_matches = []
	for matchNum, match in enumerate(regexp):
		matchNum = matchNum + 1
		for groupNum in range(0, len(match.groups())):
			groupNum = groupNum + 1
			regexp_matches.append(match.group(groupNum))
	return regexp_matches		        

isPresent = False	

ftr = [3600, 600, 1]

sentence_per_job = []
job_list = []
date_time = []
walltime_dict = {}
cputime_dict = {}
tot_jobs = 0

job_regexp = r"Job;(.+?)\."
dt_regexp = r"^(.+?) (.+?);"
walltime_regexp = r"walltime=(.+)"
cput_regexp = r"cput=(.+?) "

with open("files/" + filename,"r") as f:
	for line in f:
		if ("Job;" in line):
			### Find the match in the string
			job_find = re.finditer(job_regexp, line)
			dt_find = re.finditer(dt_regexp, line)
			### Process the matches
			job_matches = individuate_match(job_find)
			dt_matches = individuate_match(dt_find)
			### Save the matches in a list
			job_list.append(job_matches[0])
			date_time.append([job_matches[0], [dt_matches[0], dt_matches[1]]])
			#print(line)
			### Save the entire sentence for each job
			sentence_per_job.append([job_matches[0], line])
#print(sentence_per_job)
tot_cput = 0
tot_wallt = 0
for el in sentence_per_job:
	if("cput" in el[1]):
		cput_find = re.finditer(cput_regexp, el[1])
		cput_matches = individuate_match(cput_find)
		cpu_sum = sum([a*b for a,b in zip(ftr, map(int, cput_matches[0].split(':')))])
		tot_cput += sum([a*b for a,b in zip(ftr, map(int, cput_matches[0].split(':')))])
		if el[0] not in cputime_dict:
			cputime_dict[el[0]] = cpu_sum
		else:
			cputime_dict[el[0]] += cpu_sum
	if ("walltime" in el[1]):	
		walltime_find = re.finditer(walltime_regexp, el[1])	
		walltime_matches = individuate_match(walltime_find)
		walltime_sum = sum([a*b for a,b in zip(ftr, map(int, walltime_matches[0].split(':')))])
		tot_wallt = sum([a*b for a,b in zip(ftr, map(int, walltime_matches[0].split(':')))])
		if el[0] not in walltime_dict:
			walltime_dict[el[0]] = walltime_sum
		else:
			walltime_dict[el[0]] += walltime_sum
### CPU time and walltime per job
for job,cput in cputime_dict.iteritems():
	cputime_dict[job] = str(datetime.timedelta(seconds = cput))
for job,walltime in walltime_dict.iteritems():
	walltime_dict[job] = str(datetime.timedelta(seconds = walltime))
### Total CPU time
tot_cput = str(datetime.timedelta(seconds = tot_cput))
tot_wallt = str(datetime.timedelta(seconds = tot_wallt))
### Computes the total number of jobs in a file
job_dict = Counter(job_list)
for job in job_dict:
	tot_jobs+=1
### Compute the unique set of jobs
unique_jobs_list = list(set(job_list))
with open("parsed_files/" + filename + "_parsed.txt", "w") as f:
	#f.write("========================================\n\n")
	f.write("Filename: 20180201\n\nTotal number of jobs: " + "\t" + str(tot_jobs) + "\n")
	f.write("Date: " + "\t\t\t\t" + "\t" +str(date_time[0][1][0]) + "\n")
	f.write("Total CPU time: " + "\t\t" + tot_cput + "\n")
	f.write("Total Walltime: " + "\t\t" + tot_wallt + "\n\n")
	f.write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n")
	for job in unique_jobs_list:
		#f.write("========================================\n\n")
		f.write("Job ID: " + str(job) + "\n\n")
		for key,cput in cputime_dict.iteritems():
			if(job == key):
				f.write("CPU time: " + str(cput) + "\n")
		for key,wallt in walltime_dict.iteritems():
			if(job == key):
				f.write("Walltime: " + str(wallt) + "\n\n\n")	
		for line in sentence_per_job:
			if(line[0] == job):
				f.write(str(line[1]) + "\n")
		f.write("========================================\n")
		f.write("\n")
	


			