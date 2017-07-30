#
# mvfile.py
#

import os
import sys

import msvcrt
import os.path
import datetime
import time

def main():
	os.system('cls')
	
	fyle = 'C:\\Storm_Images\\NEW---TEMP\\GRL3\\'
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
	print( 'Enter ending time in EDT (24hr):' )
	print()
	print()
	endt		= int( input('\n>> ') )
	fnadjust 	= None
	crdir		= path
	
	while int(datetime.datetime.now().hour) < endt:
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