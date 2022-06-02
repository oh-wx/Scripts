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

	REPO = "./mesoscrape.config"

	obs = None
	stack = None
	
	# initialize all variables, set init and date as default, clean stack
	#
	# !!!
	def __init__(self):
		# remove old mesoscrape.config
		os.remove(Menu.REPO)
		
		# parameter list to write to config file
		Menu.obs = []
		
		# stack of menu selections for Back()
		Menu.stack =[]
		
	
	def write_config(line):
		with open("mesoscrape.config", "a") as f:
			for i in line:
				f.write(i + " ")
			f.write('\n')
			f.close()
		
	
	
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
		print( '# Wx Data Gather - 			  #' )
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
			Menu.write_config(sel)
			os.system('cls')
			return Menu.sec_menu()
		
	### bad formatting with new hazard value ###
	def sec_menu():
		sector	= {'SP':'s15',
				   'NE':'s16',
				   'EC':'s17',
				   'SE':'s18',
				   'US':'s19',
				   'MW':'s20',
				   'CP':'s14',
				   'NP':'s13',
				   'SW':'s12',
				   'NW':'s11'}
		sectors = []

		print( '#############' )
		print( '# {haz} Wx  #' )
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

		os.system('cls')
		
		return Menu.write_config(sectors)
		
	
	'''
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
	'''	
		
		
def main():
		#while(True):
		Menu()
		Menu.main_menu()
		print('\nData Grab Complete')
		input('\nPress Enter\n')


main()