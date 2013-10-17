#!/usr/bin/python

import subprocess
import os
import sys

successCounter = 0
queryCounter = 0

def execute(queryName):
	global queryCounter
	global successCounter

	queryCounter += 1
	sys.stdout.write('Executing '+queryName+'.. ')
	sys.stdout.flush()
	try:
		os.system('curl -X POST --data-urlencode "query@'+queryName+'.json" http://localhost:5000/jsonQuery')
		print('Success')
		successCounter += 1

	except Exception as err:
	    print(queryName+' failed: '+ str(err))
	    
	print('')


execute('query1')
execute('query6')

print('');
print('Executed queries: '+str(queryCounter))
print('Errors: '+str(queryCounter-successCounter))