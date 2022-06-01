import os
import sys

import urllib.request
from bs4 import BeautifulSoup
import requests
import datetime
from datetime import date, timedelta
import time


class Menu:
	### GLOBALS ###

	REPO = 'W:\\WxEvents\\NEW---TEMP\\DataGrab\\'
	DATE = None
	
	page = None
	init = None
	date = None
	SPCdate = None
	archive = None
	
	obs = None
	stack = None
	
	# initialize all variables, set init and date as default, clean stack
	#
	# !!!
	def __init__(self):
		# get init time and format date for Current Obs
		Menu.page = urllib.request.urlopen('http://www.spc.noaa.gov/exper/mesoanalysis/new/viewsector.php?sector=20').read()
		Menu.init = str( BeautifulSoup(Menu.page, 'html.parser').findAll('div', {'id': 'latest'})[0].text ).split()[1]
		Menu.archive = False
		
		Menu.SPCdate = str( BeautifulSoup(Menu.page, 'html.parser').findAll('div', {'id': 'latest'})[0].text ).split()[0]
		Menu.DATE = datetime.datetime( int("20"+Menu.SPCdate.split("/")[2]), int(Menu.SPCdate.split("/")[0]),int(Menu.SPCdate.split("/")[1]) )
		Menu.date = datetime.datetime.now()
		
		Menu.obs = {'haz':None, 'sec':None, 'day':Menu.date, 'ini':Menu.init}
		Menu.stack =[]
		
	
	### !!! ERROR with stack, Back must be selected twice !!! ###
	def back():
		os.system('cls')
		Menu.stack.pop()()

	
	def show_menu(options):
		for i in options:
			print( i + '. ' + options[i][0] )
		
		choice = input('\n>> ')
		
		if choice == '':
			print( '\nNo selection made' )
			input( 'Press Enter\n' )
			# not exiting gracefully
			#return choice
			os.system('cls')
			Menu.back()

		else:
			try:
				options[choice]
				Menu.stack.append(options[choice][1])
				os.system('cls')
				return choice
				
			except KeyError:
				print( '\nInvalid selection' )
				input( 'Press Enter\n' )
				# not exiting gracefully
				#return choice
				os.system('cls')
				Menu.back()
				
				
	def main_menu():
		options = {'1':('Observations',Menu.obs_menu),
				   '0':('Exit',exit)}
		
		Menu.stack.append(Menu.main_menu)
		os.system('cls')
		
		print( "Enter path:" )
		Menu.REPO = input( "\n>> " ) + '\\'
		print()
		
		print( '###############################' )
		print( '#							  #' )
		print( '# Wx Data Gather - '+Menu.DATE.strftime('%m/%d/%Y')+' #' )
		print( '#							  #' )
		print( '###############################' )
		print()
		print( 'Select Wx Data:' )
		
		sel = Menu.show_menu(options)
	
		return options[sel][1]()
		

	def obs_menu():
		options = ['1','2','9','R','V','P','C','H','M','D','L','I','O','S', 'A', 'E']
				   
		print( '#########################' )
		print( '#	  Observations		#' )
		print( '#						#' )
		print( '# Additional Parameters #' )
		print( '# R: Base Reflectivity	#' )
		print( '# V: Visible Satellite	#' )
		print( '# P: Precipitable Water #' )
		print( '# H: Hail Parameters	#' )
		print( '# M: MCS Maintenance	#' )
		print( '# D: Derecho Composite	#' )
		print( '# L: Max Lapse Rate		#' )
		print( '# I: Mid LR & Sfc Dewpt #' )
		print( '# O: H8-H5 Cross Over	#' )
		print( '# S: Low Level Stretch	#' )
		print( '# A: Critical Angle		#' )
		print( '# C: 850mb Convergence	#' )
		print( '# E: Eff Shr & MLCAPE	#' )
		print( '#########################' )
		print()
		print( 'Select Hazard Type' )
		print( 'Add any params separated by a space' )
		print( '1. Severe' )
		print( '2. Winter' )
		print( '9. Back' )
		
		sel = input('\n>> ').upper().split()
		sel.sort()			# must be unchained from above statement
		
		for opt in sel:
			if opt not in options:
				print( '\nInvalid selection' )
				input( 'Press Enter\n' )
				os.system('cls')
				return Menu.back()
		if sel == '9':
			os.system('cls')
			return Menu.back()
		else:
			Menu.obs['haz'] = sel
			Menu.stack.append(Menu.sec_menu)
			os.system('cls')
			return Menu.sec_menu()
		
	### bad formatting with new hazard value ###
	def sec_menu():
		'''options = {'1':('MW',Menu.day_menu),
				   '2':('EC',Menu.day_menu),
				   '3':('CP',Menu.day_menu),
				   '4':('NE',Menu.day_menu),
				   '5':('US',Menu.day_menu),
				   '6':('SP',Menu.day_menu),
				   '7':('SE',Menu.day_menu),
				   '9':('Back',Menu.back)}'''
				   
		sector	= {'SP':['SP','s15'],
				   'NE':['NE','s16'],
				   'EC':['EC','s17'],
				   'SE':['SE','s18'],
				   'US':['US','s19'],
				   'MW':['MW','s20'],
				   'CP':['CP','s14'],
				   'NP':['NP','s13'],
				   'SW':['SW','s12'],
				   'NW':['NW','s11']}
		sectors = []

		print( '#############' )
		print( '# {haz} Wx #'.format(haz='Winter' if Menu.obs['haz'][0]=='2' else 'Severe') )
		print( '#############' )
		print()
		print( 'Select Sector' )
		print( 'For multiple Sectors separate by a space' )
		print()
		print( '####################' )
		print( '#	  Sectors	   #' )
		print( '#				   #' )
		print( '# Midwest	- MW   #' )
		print( '# S. Plains - SP   #' )
		print( '# U.S.		- US   #' )
		print( '# C. Plains - CP   #' )
		print( '# Northeast - NE   #' )
		print( '# Southeast - SE   #' )
		print( '# E. Coast	- EC   #' )
		print( '# N. Plains - NP   #' )
		print( '# Southwest - SW   #' )
		print( '# Northwest - NW   #' )
		print( '####################' )

		'''sel = Menu.show_menu(options)
		Menu.obs['sec'] = options[sel][0]
				
		return options[sel][1]()'''
		
		# need to add some error checking
		inp = input('\n>> ').upper()	# maybe build array of Sectors here instead of in get_obs()
		inp = inp.split()
		
		for s in inp:
			sectors.append(sector[s])
		
		Menu.obs['sec'] = sectors
		os.system('cls')
		return Menu.day_menu()
		

	### bad formatting with new hazard value ###
	def day_menu():
		options = {'1':('Today',Menu.aut_menu)}
		# add 4 prior days to options		   
		for i in range(1,7):
			formdate = Menu.DATE + timedelta(days = -i)
			options[str(i+1)] = (formdate.strftime('%m/%d/%Y'),Menu.ini_menu)		
		options['8'] = ('Archive', Menu.ini_menu)
		options['9'] = ('Back', Menu.back)

		print( '###############' )
		print( '# {haz} -{sec}- #'.format(haz='Winter' if Menu.obs['haz'][0]=='2' else 'Severe', sec=Menu.obs['sec'][0]) )
		print( '#  ' + Menu.DATE.strftime('%m/%d/%Y') + ' #' )
		print( '###############' )
		print()
		print( 'Select Day' )

		sel = Menu.show_menu(options)
		
		# if archive day selected, get date
		if sel == '8':
			Menu.archive = True
			print( '\nEnter the Archive date (mm/dd/yyyy):' )
			date = input('\n>> ')
			date = date.split('/')
			Menu.obs['day'] = datetime.datetime(int(date[2]),int(date[0]),int(date[1]))
		else:
			Menu.obs['day'] = Menu.DATE + timedelta(days = -(int(sel)-1))

		return options[sel][1]()
		
	
	def aut_menu():
		begt = None
		dur = None
		endt = None
		
		# TEMPORARY #
		satlat = 31.32
		satlon = -97.18
		sectors = ['TX','DIX','OHV','NPL']	# array of MesoNet sector(s)

		
				   
		print( '###############' )
		print( '# {haz} -{sec}- #'.format(haz='Winter' if Menu.obs['haz'][0]=='2' else 'Severe', sec=Menu.obs['sec']) )
		print( '#  ' + Menu.obs['day'].strftime('%m/%d/%Y') + ' #' )
		print( '###############' )
		print()
		print( 'Press Enter for manual initial times' )
		print( 'B. Back' )
		print()
		
		print( 'Enter selection above' )
		print( 'For automatic data grab, enter start hour (24hr Central Time):' )
		i = input('>> ').upper()
		
		# determine selection; UGLY
		if ( i == '' ):
			os.system('cls')
			return Menu.ini_menu()
		elif ( i == 'B' ):
			os.system('cls')
			return Menu.back()
		else:
			i = int(i)
			begt = datetime.datetime(Menu.date.year, Menu.date.month, Menu.date.day, i, 0, 0)
			
			# input duration
			print()
			print( 'Enter duration in hours:' )
			dur = int( input('>> ') )
			
			### ERRORS - challenges in grabbing dynamic content from msfc.nasa.gov ###
			#print()
			#print( 'Enter URL for satellite grab or leave blank' )
			#saturl = input('>> ')
			
			# calculate end time from begin time and duration
			endt = begt + timedelta(hours =+ dur)
			curt = datetime.datetime.now()
			
			# run until current time exceeds end time
			while( curt <= endt ):
						
				# grab data after current time exceeds begin time, only grab data 45min past the hour
				if( curt >= begt):
					if( curt.minute == 45 ):
						# update initial time parameters to change file name and force default initial time when grabbing data
						Menu.page = urllib.request.urlopen('http://www.spc.noaa.gov/exper/mesoanalysis/new/viewsector.php?sector=20').read()
						Menu.init = str( BeautifulSoup(Menu.page, 'html.parser').findAll('div', {'id': 'latest'})[0].text ).split()[1]
						Menu.obs['ini'] = ''
						
						# get proper date if automation runs into new day
						Menu.SPCdate = str( BeautifulSoup(Menu.page, 'html.parser').findAll('div', {'id': 'latest'})[0].text ).split()[0]
						Menu.obs['day'] = datetime.datetime( int("20"+Menu.SPCdate.split("/")[2]), int(Menu.SPCdate.split("/")[0]),int(Menu.SPCdate.split("/")[1]) )#.strftime('%Y%m%d')
					
						Menu.get_obs()
						Menu.get_mesonet( sectors, curt+timedelta(hours =+ 5) )		# convert to UTC !!! must update for DST
						
						#Menu.get_goes16(satlat,satlon)
						
						time.sleep(3300)	# sleep for 55min until next cycle
					
					'''
					if( (curt.minute%5) == 0 ):
						#Menu.get_goes16(satlat, satlon)
						time.sleep(65)	# only grab goes16 once per 5min
					'''
					
				curt = datetime.datetime.now()
		
		
	def ini_menu():
		print( '###############' )
		print( '# {haz} -{sec}- #'.format(haz='Winter' if Menu.obs['haz'][0]=='2' else 'Severe', sec=Menu.obs['sec']) )
		print( '#  ' + Menu.obs['day'].strftime('%m/%d/%Y') + ' #' )
		print( '###############' )
		print()
		print( 'Enter Initial Time(s)' )
		print( 'Sequence times by "begin-end"' )
		print( 'Or press enter for Current ~{init}Z'.format(init=Menu.init) )

		i = input('\n>> ')
		'''
		if i == '9':
			Menu.back()
		else:
			Menu.obs['ini'] = i
		'''
		i = i.split('-')
		if len(i) > 1:
			for n in range(int(i[0]),int(i[1])+1):
				Menu.obs['ini'] = str(n)
				Menu.get_obs()
		else:
			Menu.obs['ini'] = str(i[0])
			return Menu.get_obs()
		
		return