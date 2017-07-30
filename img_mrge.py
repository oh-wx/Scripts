###############
# Image Merge #
###############


import os
import sys

from PIL import Image
import datetime
from datetime import timedelta
import time
import requests

REPO = 'C:/Scripts/OH-Wx/'
#DATE = datetime.datetime.now()

###
#
# URLs:
#	1Km VIS OH - http://climate.cod.edu/data/satellite/1km/Indiana_Ohio/vis/Indiana_Ohio.vis.20170720.0115.gif
#
#	
#	2Km VIS VA - http://climate.cod.edu/data/satellite/2km/VA_WV/vis/VA_WV.vis.20170720.1700.gif
#	2Km MAP VA - http://climate.cod.edu/data/satellite/2km/VA_WV/maps/VA_WV_map.gif

def main():
	os.system('cls')
	today = datetime.datetime.now()
	#print( 'Enter overlay img path:' )
	#TKmfg = Image.open( input('\n>> ') ).convert('RGBA')	#Image.open(REPO + 'map.gif').convert('RGBA')
	#TKmbg = Image.open(REPO + '2Km-IL.gif')	#Image.open(REPO + 'vis.gif').convert('RGBA')
	
	fg = Image.open(REPO + '1Km-OH.gif').convert('RGBA')
	
	print( 'Enter desitnation ("\\" req):' )
	path = input('>> ')
	print( '\nEnter start time in GMT (24hr):' )
	print( '[earliest archive -3.5hrs]' )
	begt = int( input('>> ') )
	print( '\nEnter end time in GMT (24hr):' )
	endt = int( input('>> ') )
	
	# adjust to for loop with 15min interval between start and end times
	# account for day roll-over at 0000Z
	# earliest archive is -3.5hrs; add fail-safe
	# don't need much time formatting from 'now'

	for min in range(
		fyle = 'VISSAT~{time}Z-OH-{date}.png'.format(		)
		path = path + fyle
		url = 'http://climate.cod.edu/data/satellite/1km/Indiana_Ohio/vis/Indiana_Ohio.vis.{date}.{time}.gif'.format(date=dgmt, time=tgmt)
		with open(path, 'wb') as f:
				f.write( requests.get(url).content )		
		print(fyle)

		bg = Image.open( path ).convert('RGBA')
		bg.paste(fg, None, fg)
		# save in PNG for lower data loss
		bg.save(path,'PNG')
			
	
	
	

main()