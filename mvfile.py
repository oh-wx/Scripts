#
# mvfile.py
#

import os
import sys

import msvcrt
import os.path
import datetime
from datetime import date, timedelta
import time

def main():
	os.system('cls')
	
	fyle = 'C:\\WxEvents\\NEW---TEMP\\GR3\\'
	path = None
	
	
	print( '##################' )
	print( '#                #' )
	print( '# MV File Cycler #' )
	print( '#                #' )
	print( '##################' )
	print()
	
	#print( 'Enter source dir ("\" req):' )
	#fyle = input('\n>> ')
	
	print( 'Enter desitnation ("\\" req):' )
	path 		= input('\n>> ')
	print( 'Enter duration in hrs:' )
	print()
	print()
	dur			= int( input('\n>> ') )
	fnadjust 	= None
	crdir		= path
	
	begt = datetime.datetime.now()
	endt = begt + timedelta(hours =+ dur)
	
	while datetime.datetime.now() < ( datetime.datetime.now()+timedelta(hours =+ dur) ):
		try:
			#if int(datetime.datetime.now().hour) < endt:
			for fname in os.listdir(fyle):
				if fname.endswith('.png'):
					time.sleep(3)
					#print( 'file' )
					'''
					 fnadjust = fname.split('_')
					
					if not os.path.exists( crdir + fnadjust[0].upper() ):
						os.makedirs(crdir + fnadjust[0].upper() )
					'''
					now = datetime.datetime.now()
					now = now.strftime('%H%M%S')
					filename = os.listdir(fyle)[0]
					os.rename(fyle+filename, path+now+'-'+filename)
						
		except OSError as e:
			print( str(e.message) )
			
main()