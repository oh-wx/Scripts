import os
import sys

import urllib.request
from bs4 import BeautifulSoup
import requests
import datetime
from datetime import date, timedelta


### TO-DO ###
#
#	implement VISSAT and RDR capability
#	implement Twisterdata sauce
#	



class Menu:
	### GLOBALS ###
	REPO = 'C:\\Storm_Images\\NEW---TEMP\\OH-Wx_DataGrab'
	DATE = datetime.datetime.now()
	
	# get init time for Current Obs and set as default
	page = urllib.request.urlopen('http://www.spc.noaa.gov/exper/mesoanalysis/new/viewsector.php?sector=20').read()
	init = str( BeautifulSoup(page, 'html.parser').findAll('div', {'id': 'latest'})[0].text ).split( )[1]
	
	obs = {'haz':None, 'sec':None, 'day':None, 'ini':init}
	mdl = {'mdl':None, 'ini':None, 'src':None}
	stack = []
	
	
	def write_file(url, fyle):
		path = Menu.REPO + '/' + fyle
		with open(path, 'wb') as f:
				f.write( requests.get(url).content )		
		print(fyle)
	
	
	### !!! ERROR with stack, Back must be selected twice !!! ###
	def back():
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
			except KeyError:
				print( '\nInvalid selection' )
				input( 'Press Enter\n' )
				# not exiting gracefully
				#return choice
				os.system('cls')
				Menu.back()
				
		Menu.stack.append(options[choice][1])
		os.system('cls')
		return choice
	
	
	def get_obs():
		### Curr:	http://www.spc.noaa.gov/exper/mesoanalysis/{sector}/{param}/{param}.gif					## NOTE: for filled colors {param}_sf.gif
		### Past:	http://www.spc.noaa.gov/exper/mesoanalysis/{sector}/{param}/{param}_{date}{init}.gif	## NOTE: oldest image is -4 days to the init
		### Past OBS:  http://www.spc.noaa.gov/exper/mesoanalysis/{sector}/{param}/sfc_{date}_{init}00.gif
		### Rdr :	http://www.spc.noaa.gov/exper/mesoanalysis/{sector}/rgnlrad/rgnlrad.gif
		### Vis :	http://www.spc.noaa.gov/exper/mesoanalysis/{sector}/1kmv/1kmv.gif

		
		# atmospheric parameters to gather
		surface = [('OBS','bigsfc'),
				   ('PRS','pmsl'),
				   ('DEWPT','ttd',True),
				   ('SBVORT','dvvr',True)]
		
		winds   = [('925mb','925mb',True),
				   ('850mb','850mb',True),
				   ('700mb','700mb',True),
				   ('500mb','500mb',True),
				   ('300mb','300mb',True),
				   ('H5VORT','vadv',True),
				   ('H3CIRC','ageo',True)]
				   
		thermo  = [('SBCAPE','sbcp',True),
				   ('MLCAPE','mlcp',True),
				   ('MUCAPE','mucp',True),
				   ('MLR','laps',True),
				   ('LLR','lllr',True),
				   ('LCL','lclh',True)]
				   
		shear	= [('6KmSHR','shr6'),
				   ('8KmSHR','shr8'),
				   ('1KmSHR','shr1'),
				   ('EFFSHR','eshr'),
				   ('EFFSRH','effh'),
				   ('3KmSRH','srh3'),
				   ('1KmSRH','srh1'),
				   ('9-11KmSHR','ulsr')]
				   
		comp	= [('SCCOMP','scp'),
				   ('SIGTOR','stpc'),
				   ('1KmEHI','ehi1'),
				   ('3KmEHI','ehi3'),
				   ('DERCHO','dcp')]
				   
		frozen	= [('SFCTEMP','fztp'),
				   ('SFCBULB','swbt'),
				   ('MAXBULB','mxwb')]
				   
		radar	= [('BR','rgnlrad')]	# must match standardized data struct above
		
		vissat	= [('VISSAT','1kmv')]	# must match standardized data struct above
		
		severe  = (surface, winds, thermo, shear, comp)
		winter  = (surface, winds, frozen)
		
		# dictionaries for Obs Menu selection
		sector  = {'NE':'s16', 'EC':'s17', 'MW':'s20', 'US':'s19'}
		haz 	= {'Severe':severe, 'Winter': winter, 'Radar':radar, 'Vis Sat':vissat}
		
		# get obs data to build URL
		hazard = haz[Menu.obs['haz']]	#severe if Menu.obs['haz']=='Severe' else winter
		sector = sector[Menu.obs['sec']]
		current = True if 'Current' in Menu.obs['day'] else False
		past = Menu.obs['day'][8:] + Menu.obs['day'][:2] + Menu.obs['day'][3:5]
		formdate = Menu.DATE.strftime('%Y%m%d') if current else (Menu.obs['day'][6:]+Menu.obs['day'][:2]+Menu.obs['day'][3:5])
		
		# grab data!
		for i in range(len(hazard)):
			for n in range(len(hazard[i])):
				if current:
					# less ugly conditional for filled color images
					if len(hazard[i][n]) == 3:
						url  = 'http://www.spc.noaa.gov/exper/mesoanalysis/{sector}/{param}/{param}_sf.gif'.format(sector=sector, param=hazard[i][n][1])
					else:
						url  = 'http://www.spc.noaa.gov/exper/mesoanalysis/{sector}/{param}/{param}.gif'.format(sector=sector, param=hazard[i][n][1])
				else:
					url = 'http://www.spc.noaa.gov/exper/mesoanalysis/{sector}/{param}/{param}_{date}{init}'	\
					.format(sector=sector, param=hazard[i][n][1], date=past, init=Menu.obs['ini']) + '.gif'
					
					# must use different URL for Past OBS
					if hazard[i][n][0] == 'OBS':
						url = 'http://www.spc.noaa.gov/exper/mesoanalysis/{sector}/{param}/sfc_{date}_{init}'	\
						.format(sector=sector, param=hazard[i][n][1], date=past, init=Menu.obs['ini']) + '00.gif'

				fyle = hazard[i][n][0] + '~{init}Z-'.format(init=Menu.obs['ini']) + Menu.obs['sec'] + '-' + formdate + '.gif'
				Menu.write_file(url, fyle)
				
				
	def get_obs2():
		### Curr:	http://www.spc.noaa.gov/exper/mesoanalysis/{sector}/{param}/{param}.gif					## NOTE: for filled colors {param}_sf.gif
		### Past:	http://www.spc.noaa.gov/exper/mesoanalysis/{sector}/{param}/{param}_{date}{init}.gif	## NOTE: oldest image is -4 days to the init
		### Past OBS:  http://www.spc.noaa.gov/exper/mesoanalysis/{sector}/{param}/sfc_{date}_{init}00.gif
		### Rdr :	http://www.spc.noaa.gov/exper/mesoanalysis/{sector}/rgnlrad/rgnlrad.gif
		### Vis :	http://www.spc.noaa.gov/exper/mesoanalysis/{sector}/1kmv/1kmv.gif

		
		# atmospheric parameters to gather
		petig	= [('OBS','bigsfc'),
				   ('PRS','pmsl'),
				   ('DEWPT','ttd',True),
				   ('925mb','925mb',True),
				   ('850mb','850mb',True),
				   ('700mb','700mb',True),
				   ('500mb','500mb',True),
				   ('300mb','300mb',True),
				   ('H5VORT','vadv',True),
				   ('H3CIRC','ageo',True)]
				   
		thermo  = [('SBCAPE','sbcp',True),
				   ('MLCAPE','mlcp',True),
				   ('MUCAPE','mucp',True),
				   ('MLR','laps',True),
				   ('LLR','lllr',True),
				   ('LCL','lclh',True)]
				   
		shear	= [('6KmSHR','shr6'),
				   ('8KmSHR','shr8'),
				   ('1KmSHR','shr1'),
				   ('EFFSHR','eshr'),
				   ('EFFSRH','effh'),
				   ('3KmSRH','srh3'),
				   ('1KmSRH','srh1'),
				   ('9-11KmSHR','ulsr'),
				   ('SBVORT','dvvr',True)]
				   
		comp	= [('SCCOMP','scp'),
				   ('SIGTOR','stpc'),
				   ('1KmEHI','ehi1'),
				   ('3KmEHI','ehi3')]
				   
		frozen	= [('SFCTEMP','fztp'),
				   ('SFCBULB','swbt'),
				   ('MAXBULB','mxwb')]
				  
		severe  = petig + thermo + shear + comp
		winter  = petig + frozen
		
		# dictionaries for Obs Menu selection
		sector  = {'NE':'s16', 'EC':'s17', 'MW':'s20', 'US':'s19'}
		haz 	= {'Severe':severe, 'Winter': winter}
		special	= {'1':severe,
				   '2':winter,
				   'D':('DERCHO','dcp'),
				   'P':('PWAT','pwtr',True),
				   'B':('BR','rgnlrad'),
				   'V':('VISSAT','1kmv')}
		
		# get obs data to build URL
		hazard = Menu.obs['haz'].split()[0]
		sector = sector[Menu.obs['sec']]
		current = True if 'Current' in Menu.obs['day'] else False
		past = Menu.obs['day'][8:] + Menu.obs['day'][:2] + Menu.obs['day'][3:5]
		formdate = Menu.DATE.strftime('%Y%m%d') if current else (Menu.obs['day'][6:]+Menu.obs['day'][:2]+Menu.obs['day'][3:5])
		parameter = []
		
		# build Custom parameter list or use one of the defaults
		if hazard == 'Custom':
			hazard = Menu.obs['haz'].split()
			hazard.remove('Custom')
			hazard.sort()
			
			if hazard[0]=='1' or hazard[0]=='2':
				parameter = special[hazard[0]]	# assign default list to parameter for append below
				hazard.pop(0)					# remove default list from hazard list
				
			for item in hazard:
				parameter.append(special[item])
		else:
			parameter = haz[hazard]
		
		# grab data!
		for i in range(len(parameter)):
			url = 'http://www.spc.noaa.gov/exper/mesoanalysis/{sector}/{param}/'.format(sector=sector, param=parameter[i][1])
			if current:
				url += parameter[i][1]
				
				# less ugly conditional for filled color images
				if len(parameter[i]) == 3:
					url += '_sf'
					
			else:
				# must use different URL for Past OBS
				if parameter[i][0] == 'OBS':
					url += 'sfc_' + past + '_' + Menu.obs['ini'] + '00'
				elif parameter[i][0] == 'BR':
					url += 'rad_' + formdate + '_' + Menu.obs['ini'] + '00'
				elif parameter[i][0] == 'VISSAT':
					url += 'vis_' + formdate + '_' + Menu.obs['ini'] + '00'
				else:
					url += parameter[i][1] + '_' + past + Menu.obs['ini']

			url += '.gif'
			
			fyle = parameter[i][0] + '~{init}Z-'.format(init=Menu.obs['ini']) + Menu.obs['sec'] + '-' + formdate + '.gif'
			Menu.write_file(url, fyle)
		
	# --------- end get_obs2() ---------- #
	
	def get_psu():
		print( '#############' ) if Menu.mdl['mdl']=='EURO' else print( '############' )	# stupid formatting conditionals
		print( '# {mdl} ~{init} #'.format(mdl=Menu.mdl['mdl'], init=Menu.mdl['ini']) )
		print( '#############' ) if Menu.mdl['mdl']=='EURO' else print( '############' )	# stupid formatting conditionals
		print( '\nEnter Forecast Hours\n' )
		
		# get Model data to build URL
		start	= int( input('Starting hour >>  ') )
		stop 	= int( input('Ending hour   >>  ') )
		models 	= {'EURO':('ECMWF_','ECMWF0.5_'), 'CMC':('CMC_','CMCNA_'), 'GFS':('MRF_','')}
		model  	= Menu.mdl['mdl']
		init 	= '0z' if Menu.mdl['ini']=='00Z' else Menu.mdl['ini'].lower().strip('0')	# format init time for URL
		interval = 12
		
		if model=='CMC' and init=='12z':
			url = models[model][1] + init
		else:
			url = models[model][0] + init

		if model == 'EURO':
			interval = 24

		# grab data!
		for i in range(start, stop+interval, interval):
			if model=='EURO' and i>168:
				url = models[model][1] + init

			image = 'http://mp1.met.psu.edu/~fxg1/{model}/f{hr}.gif'.format(hr=i, model=url)
			fyle = '{hr}hr_{model}-{init}Z-'.format( hr=i, model=model, init=init.strip('z').zfill(2) ) + Menu.DATE.strftime('%Y%m%d') + '.gif'
			Menu.write_file(image, fyle)
		
		
	def get_twd():
		print('get TWD data')

		
	def main_menu():
		options = {'1':('Observations',Menu.obs_menu),
				   '2':('Models',Menu.mdl_menu),
				   '0':('Exit',exit)}
		
		Menu.stack.append(Menu.main_menu)
		os.system('cls')
		
		print( '###############################' )
		print( '#                             #' )
		print( '# Wx Data Gather - '+Menu.DATE.strftime('%m/%d/%Y')+' #' )
		print( '#                             #' )
		print( '###############################' )
		print()
		print( 'Select Wx Data:' )

		sel = Menu.show_menu(options)
		
		return options[sel][1]()
	
	def obs_menu():
		options = {'1':('Severe', Menu.haz_menu),
				   '2':('Winter', Menu.haz_menu),
				   '3':('Custom', Menu.cus_menu),
				   '9':('Back',   Menu.back)}
		
		print( '################' )
		print( '# Observations #' )
		print( '################' )
		print()
		print( 'Select Hazard Type' )

		sel = Menu.show_menu(options)
		Menu.obs['haz'] = options[sel][0]

		return options[sel][1]()
		
	
	def cus_menu():
		options = ['1','2','9','B','V','P','D']
				   
		print( '#########################' )
		print( '#     Observations      #' )
		print( '#                       #' )
		print( '# Additional Parameters #' )
		print( '# B: Base Reflectivity  #' )
		print( '# V: Visible Satellite  #' )
		print( '# P: Precipitable Water #' )
		print( '# D: Derecho Composite  #' )
		print( '#########################' )
		print()
		print( 'Select Hazard Type' )
		print( 'Add any params separated by a space' )
		print( '1. Severe' )
		print( '2. Winter' )
		print( '9. Back' )
		
		sel = input('\n>> ').upper()
		
		if not any(opt in sel.split() for opt in options):
			print( '\nInvalid selection' )
			input( 'Press Enter\n' )
			os.system('cls')
			Menu.back()
		elif sel == '9':
			os.system('cls')
			Menu.back()
		else:
			Menu.obs['haz'] += ' ' + sel
			Menu.stack.append(Menu.haz_menu)
			os.system('cls')
			Menu.haz_menu()
		
		
	def haz_menu():
		options = {'1':('NE',Menu.day_menu),
				   '2':('MW',Menu.day_menu),
				   '3':('EC',Menu.day_menu),
				   '4':('US',Menu.day_menu),
				   '9':('Back',Menu.back)}

		print( '#############' )
		print( '# {haz} Wx #'.format(haz=Menu.obs['haz'].split()[0]) )	# use split for formatting
		print( '#############' )
		print()
		print( 'Select Sector' )

		sel = Menu.show_menu(options)
		Menu.obs['sec'] = options[sel][0]
				
		return options[sel][1]()
		
	
	# !!! Adjust function back to get_obs() !!!
	
	def day_menu():
		options = {'1':('Current ~{ini}Z'.format(ini=Menu.obs['ini']),Menu.get_obs2)}
		# add 4 prior days to options menu		   
		for i in range(1,5):
			formdate = Menu.DATE + timedelta(days = -i)
			options[str(i+1)] = (formdate.strftime('%m/%d/%Y'),Menu.ini_menu)		
		options['9'] = ('Back', Menu.back)
		

		print( '###############' )
		print( '# {haz} -{sec}- #'.format(haz=Menu.obs['haz'].split()[0], sec=Menu.obs['sec']) )	# use split for formatting
		print( '#  ' + Menu.DATE.strftime('%m/%d/%Y') + ' #' )
		print( '###############' )
		print()
		print( 'Select Day' )

		sel = Menu.show_menu(options)
		Menu.obs['day'] = options[sel][0]

		return options[sel][1]()
		
	
	def ini_menu():
		print( '###############' )
		print( '# {haz} -{sec}- #'.format(haz=Menu.obs['haz'], sec=Menu.obs['sec']) )
		print( '#  ' + Menu.obs['day'] + ' #' )
		print( '###############' )
		print()
		print( 'Select Initial Time' )
		
		Menu.obs['ini'] = input('\n>> ')
		
		return Menu.get_obs2()
		
		
	def mdl_menu():
		options = {'1':('EURO', Menu.mdl_init),
				   '2':('CMC',  Menu.mdl_init),
				   '3':('GFS',  Menu.mdl_init),
				   '4':('NAM',  Menu.mdl_init),
				   '5':('RAP',  Menu.mdl_init),
				   '9':('Back', Menu.back)}
		
		print( '##########' )
		print( '# Models #' )
		print( '##########' )
		print()
		print( 'Select Model' )
		
		sel = Menu.show_menu(options)
		Menu.mdl['mdl'] = options[sel][0]
		
		return options[sel][1]()
	
	
	def mdl_init():
		std_run = ('00Z', '12Z')
		off_run = ('06Z', '18Z')
		options = {}
		shift = 0	# shift the menu index to avoid overwriting
		
		# build options specific for EURO/CMC and GFS/NAM
		for i in range( len(std_run) ):
			options[str(i+shift+1)] = (std_run[i],Menu.mdl_sauc)
			if Menu.mdl['mdl']=='GFS' or Menu.mdl['mdl']=='NAM':
				options[str(i+shift+2)] = (off_run[i],Menu.mdl_sauc)
				shift = 1
		
		# add Back option since menu was dynamically generated
		options.update({'9':('Back',Menu.back)})
		
		print( '########' ) if Menu.mdl['mdl']=='EURO' else print( '#######' )	# stupid formatting conditionals
		print( '# {mdl} #'.format(mdl=Menu.mdl['mdl']) ) 
		print( '########' ) if Menu.mdl['mdl']=='EURO' else print( '#######' )	# stupid formatting conditionals
		print()
		
		sel = Menu.show_menu(options)
		Menu.mdl['ini'] = options[sel][0]
		
		return options[sel][1]()
	
	
	def mdl_sauc():
		options = {'1':('PSU Ewall',  Menu.get_psu),
				   '2':('Twisterdata',Menu.get_twd)}
		
		# cumbersome conditional to determine sauce, majority are dependent
		if Menu.mdl['mdl'] == 'GFS':
			print( '#############' )
			print( '# GFS - {init} #'.format(init=Menu.mdl['ini']) )
			print( '#############' )
			print()
			
			sel = Menu.show_menu(options)
			Menu.mdl['src'] = options[sel][0]
			
			return options[sel][1]()
			
		elif Menu.mdl['mdl']=='EURO' or Menu.mdl['mdl']=='CMC':
			Menu.mdl['src'] = 'PSU Ewall'
			return Menu.get_psu()
			
		elif Menu.mdl['mdl']=='NAM' or Menu.mdl['mdl']=='RAP':
			Menu.mdl['src'] = 'Twisterdata'
			return Menu.get_twd()
	
		
def main():

	Menu.main_menu()

	print('\ncomplete\n')
	
main()