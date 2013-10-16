#!/usr/bin/python

import subprocess
import os
import sys

def execute(queryName):
	sys.stdout.write('Executing '+queryName+'.. ')
	sys.stdout.flush()
	try:
		os.system('curl -X POST --data-urlencode "query@'+queryName+'.json" http://localhost:5000/jsonQuery > /dev/null')
	except Exception as err:
	    print(queryName+' failed: '+ str(runner.std_err))
	    exit(1)
	print('Success')

execute('query1')