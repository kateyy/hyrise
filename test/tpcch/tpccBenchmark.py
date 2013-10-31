#!/usr/bin/python

import subprocess
import os
import sys

# counts number of successful executed queries
successCounter = 0
# counts number of executed queries
queryCounter = 0

def execute(queryName):
	filePath = os.path.dirname(__file__)+'/'+queryName+'.json'

	# do not execute not existing queries
	if not os.path.exists(filePath):
		return

	global queryCounter
	global successCounter

	queryCounter += 1
	sys.stdout.write('Executing '+queryName+'.. ')
	sys.stdout.flush()

	# executing
	try:
		os.system('curl -X POST --data-urlencode "query@'+filePath+'" http://localhost:5000/jsonQuery')
		print('Success')
		successCounter += 1

	except Exception as err:
	    print(queryName+' failed: '+ str(err))
	    
	print('')

# executing query 1-22
for i in range(1,23):
	execute('query'+str(i))

print('');
print('Executed queries: '+str(queryCounter)+'/22')
print('Errors: '+str(queryCounter-successCounter))