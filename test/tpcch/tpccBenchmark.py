#!/usr/bin/python

import subprocess
import os
import sys
import envoy

# counts number of successful executed queries
successCounter = 0
# counts number of executed queries
queryCounter = 0

def getExecutionTime(response, theFile):
	count = response.count("duration")
	exeTime = 0
	startTimeIndex = 0

	theFile.write("")

	# count-1 to ignore the response time
	for i in range(count-1):
		startTimeIndex = response.find("duration", startTimeIndex+1)
		startIdIndex = response.find("id", startTimeIndex+1)
		endTimeIndex = response.find(",", startTimeIndex+1)
		endIdIndex = response.find(",", startIdIndex+1)

		theFile.write('\t'+response[startIdIndex+4:endIdIndex]+': '+response[startTimeIndex+10:endTimeIndex]+'\n')
		exeTime += int(response[startTimeIndex+10:endTimeIndex])


	startTimeIndex = response.find("duration", startTimeIndex+1)
	startIdIndex = response.find("id", startTimeIndex+1)
	endTimeIndex = response.find(",", startTimeIndex+1)
	endIdIndex = response.find(",", startIdIndex+1)

	theFile.write('\t------\n\tOverall time: '+str(exeTime)+'\n\n')
	theFile.write('\t('+response[startIdIndex+4:endIdIndex]+': '+response[startTimeIndex+10:endTimeIndex]+'\n')
	theFile.write('\tOverall time: '+str(exeTime+int(response[startTimeIndex+10:endTimeIndex]))+')\n\n\n')
	return exeTime

def execute(queryName, theFile):
	filePath = os.path.dirname(__file__)+'/'+queryName+'.json'

	# do not execute not existing queries
	if not os.path.exists(filePath):
		return

	global queryCounter
	global successCounter

	queryCounter += 1
	theFile.write('Result '+queryName+':\n\n')
	sys.stdout.write('Executing '+queryName+'.. ')
	sys.stdout.flush()

	# executing
	try:
		runner = envoy.run('curl -X POST --data-urlencode "query@'+filePath+'" http://localhost:5000/jsonQuery')

		if (runner.status_code == 0):
			print('Success ('+str(getExecutionTime(runner.std_out, theFile))+')')
			successCounter += 1
		else:
			print(' failed: '+ str(runner.std_err))
			theFile.write('Execution threw an error: '+str(runner.std_err))

	except Exception as err:
		print(queryName+' failed: '+ str(err))
		theFile.write('Execution threw an error: '+str(err))

print('');

# executing query 1-22
outFile = open("result.txt", "w")

for i in range(1,23):
	execute('query'+str(i), outFile)

outFile.close()

print('');
print('Executed queries: '+str(queryCounter)+'/22')
print('Errors: '+str(queryCounter-successCounter))