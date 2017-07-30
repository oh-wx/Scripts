
import os
import sys


import requests
import datetime
from datetime import timedelta
from PIL import Image


TKmURL = 'http://climate.cod.edu/data/satellite/2km/IL_IN/vis/IL_IN.vis.'	#{yyyymmdd}.{hhmm}.gif'
REPO = 'C:/Users/anwalters/Scripts/'

def main():
	os.system('cls')
	today = datetime.datetime.now()
	date = today.strftime('%Y%m%d')
	path = REPO + 'Images/vis/'
	
	# final img is based on map type, not URL; probably a result from the bg.paste(...) overlaying below
	fg = Image.open(REPO + '2KmMap.gif').convert('RGBA')
	
	print( '#############################' )
	print( '#                           #' )
	print( '# COD Meteorology Satellite #' )
	print( '#                           #' )
	print( '#############################' )
	
	
	print( '\nEnter starting time (hhmm):' )
	s = input('>> ')
	s = datetime.datetime(today.year,today.month,today.day,int(s[:2]),int(s[2:]))
	
	print( '\nEnter ending time (hhmm):' )
	e = input('>> ')
	e = datetime.datetime(today.year,today.month,today.day,int(e[:2]),int(e[2:]))
	print()
	
	if not os.path.exists(path):
		os.makedirs(path)
	
	# range of total minutes e-s; increments of 15min
	for m in range(0,int((e-s).seconds/60)+15,15):
		i = s + timedelta(minutes=+m)
		time = str(i.hour).zfill(2) + str(i.minute).zfill(2)

		url  = TKmURL + '{date}.{time}.gif'.format(date=date,time=time)
		bg   = Image.open( requests.get(url, stream=True).raw ).convert('RGBA')
		bg.paste(fg, None, fg)
		
		# save in PNG for lower data loss
		fyle = 'VISSAT~{time}Z-2Km-{date}.png'.format(time=time,date=date)
		bg.save(path + fyle,"PNG")
		

main()