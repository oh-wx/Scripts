import os
import sys

import urllib.request
from bs4 import BeautifulSoup
import requests
import datetime
from datetime import date, timedelta


### TO-DO ###
#
#	implement Twisterdata sauce
#	



class Menu:
	### GLOBALS ###
	REPO = 'C:\\Storm_Images\\NEW---TEMP\\DataGrab'
	DATE = datetime.datetime.now()
	
	# get init time for Current Obs and set as default
	page = urllib.request.urlopen('http://www.spc.noaa.gov/exper/mesoanalysis/new/viewsector.php?sector=20').read()
	init = str( BeautifulSoup(page, 'html.parser').findAll('div', {'id': 'latest'})[0].text ).split()[1]
	
	obs = {'haz':None, 'sec':None, 'day':None, 'ini':init}
	mdl = {'mdl':None, 'ini':None, 'src':None}
	stack = []
	
	
	def write_file(url, fyle):
		path = Menu.REPO + '/' + fyle
		with open(path, 'wb') as f:
				f.write( requests.get(url).content )		
		print(fyle)
	
	'''
		Potential expansion
	def grab_data(start, stop, interval, url):
	'''	
		
	
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

		# atmospheric parameter dictionaries
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
				   ('MAXLR','maxlr'),
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
		sector  = {'SP':'s15','NE':'s16','EC':'s17','SE':'s18','US':'s19','MW':'s20'}
		hazard	= {'1':severe,
				   '2':winter,
				   'D':('DERCHO','dcp'),
				   'P':('PWAT','pwtr',True),
				   'C':('HGHCHG','500mb_chg',True),
				   'M':('MCSPRB','mcsm'),
				   'H':('HAIL','hail'),
				   'B':('BR','rgnlrad'),
				   'V':('VISSAT','1kmv'),
				   'L':('MLRDEW','tdlr', True)}
		
		# get obs data to build URL
		sector = sector[Menu.obs['sec']]
		current = True if 'Current' in Menu.obs['day'] else False
		past = Menu.obs['day'][8:] + Menu.obs['day'][:2] + Menu.obs['day'][3:5]
		formdate = Menu.DATE.strftime('%Y%m%d') if current else (Menu.obs['day'][6:]+Menu.obs['day'][:2]+Menu.obs['day'][3:5])
		parameter = []
		
		# build parameter list
		if Menu.obs['haz'][0]=='1' or Menu.obs['haz'][0]=='2':
			parameter = hazard[Menu.obs['haz'][0]]		# assign default list to parameter for append below
			Menu.obs['haz'].pop(0)						# remove default list from hazard list
				
		for item in Menu.obs['haz']:
			parameter.append(hazard[item])

		# grab data!
		for i in range(len(parameter)):
			url = 'http://www.spc.noaa.gov/exper/mesoanalysis/{sector}/{param}/'.format(sector=sector, param=parameter[i][1])
			if current:
				url += parameter[i][1]
				
				# less ugly conditional for filled color images
				if len(parameter[i]) == 3:
					url += '_sf'
					
			else:
				# must use different URL for Past OBS, BR, and VISSAT
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
		
	# --------- end get_obs() ---------- #
	
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
		#################################################################################
		#                              		Severe                                    	#	
		#																			   	#
		# winds:	10m		temps:	10m		shear:	SRH 0-1Km		motion:	SR Motion  	#
		#			925mb							SRH 0-3Km				10m Inflow 	#
		#			850mb	dewpt:	10m				EHI 0-1Km						   	#
		#			700mb							EHI 0-3Km						   	#
		#			500mb	insta:	CAPE			500mb Cross						   	#
		#			300mb			CIN				850/925mb Cross ??? 			   	#
		#################################################################################

		#################################################################################
		#									Winter										#
		#																				#
		# winds:	10m		temps:	10m		dewpt:	700mb RH							#
		#			925mb			925mb			PWAT								#
		#			850mb			850mb			925/850mb ???						#
		#			700mb			MAXTEMP												#
		#			500mb																#
		#			300mb																#
		#################################################################################
		
		'''
		URL = 'http://www.twisterdata.com/data/models/gfs/3/maps/2016/12/19/06/GFS_3_2016121906_F120_TMPF_2_M_ABOVE_GROUND.png'
			  'http://www.twisterdata.com/data/models/rap/255/maps/2017/02/07/12/RAP_255_2017020712_F00_TMPF_2_M_ABOVE_GROUND.png'
			  'http://www.twisterdata.com/data/models/nam/221/maps/2017/02/07/12/NAM_221_2017020712_F00_TMPF_2_M_ABOVE_GROUND.png'
		
		
		 NOTES:  levels are a little finicky
					SRM 				- '6000_M'
					EHI/SRH/PWAT/LCL 	- 'SURFACE'
					LIFT 				- '500_1000_MB'
					MAXTEMP 			- 'SFC_500MB
		'''
	
		# winds use 10M ABOVE GROUND, temp/dewpt use 2M ABOVE GROUND
		levels	= [('SFC','2_M_ABOVE_GROUND','10_M_ABOVE_GROUND','SURFACE'),
				   ('925mb','925_MB'),
				   ('850mb','850_MB'),
				   ('700mb','700_MB'),
				   ('500mb','500_MB'),
				   ('300mb','300_MB')]
				  
		petig	= [('WIND','WSPD'),
				   ('TEMP','TMPF','TMPC'),
				   ('DEWPT','DPTF','DPTC'),
				   ('RH','RH'),
				   ('PWAT','PWATIN')]
				  
		therm	= [('CAPE','CAPE'),
				   ('CIN','CIN'),
				   ('1KmEHI','EHI1'),
				   ('3KmEHI','EHI3'),
				   ('LCL','ZLCLM'),
				   ('LIFT','LFTX')]
				   
		shear	= [('VORT','RELV'),
				   ('1KmSRH','HLCY1'),
				   ('3KmSRH','HLCY3'),
				   ('SHR','SHRM'),
				   ('MOTION','SRWSPD')]
				   
		wintr	= [('MAXTEMP','TVMXC')]
				   
		
		severe = (petig, therm, shear)
		
		winter = (petig, wintr)
				  
		
		print( '### TEST ###' )
		print( 'TwisterData has not been implemented' )
		print( str(model) + ' ' + str(init) )
	
	# --------- end get_twd() ---------- #
		
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
		options = ['1','2','9','B','V','P','C','H','M','D','L']
				   
		print( '#########################' )
		print( '#     Observations      #' )
		print( '#                       #' )
		print( '# Additional Parameters #' )
		print( '# B: Base Reflectivity  #' )
		print( '# V: Visible Satellite  #' )
		print( '# P: Precipitable Water #' )
		print( '# C: 12hr 500MB Change	#' )
		print( '# H: Hail Parameters	#' )
		print( '# M: MCS Maintenance	#' )
		print( '# D: Derecho Composite  #' )
		print( '# L: Mid LR & Sfc Dewpt #' )
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
				Menu.back()
		if sel == '9':
			os.system('cls')
			Menu.back()
		else:
			Menu.obs['haz'] = sel
			Menu.stack.append(Menu.haz_menu)
			os.system('cls')
			Menu.haz_menu()
		
	### bad formatting with new hazard value ###
	def haz_menu():
		options = {'1':('MW',Menu.day_menu),
				   '2':('EC',Menu.day_menu),
				   '3':('NE',Menu.day_menu),
				   '4':('US',Menu.day_menu),
				   '5':('SP',Menu.day_menu),
				   '6':('SE',Menu.day_menu),
				   '9':('Back',Menu.back)}

		print( '#############' )
		print( '# {haz} Wx #'.format(haz=Menu.obs['haz'][0]) )
		print( '#############' )
		print()
		print( 'Select Sector' )

		sel = Menu.show_menu(options)
		Menu.obs['sec'] = options[sel][0]
				
		return options[sel][1]()
		

	### bad formatting with new hazard value ###
	def day_menu():
		options = {'1':('Current ~{ini}Z'.format(ini=Menu.obs['ini']),Menu.get_obs)}
		# add 4 prior days to options menu		   
		for i in range(5):
			formdate = Menu.DATE + timedelta(days = -i)
			options[str(i+2)] = (formdate.strftime('%m/%d/%Y'),Menu.ini_menu)		
		options['9'] = ('Back', Menu.back)

		print( '###############' )
		print( '# {haz} -{sec}- #'.format(haz=Menu.obs['haz'][0], sec=Menu.obs['sec']) )
		print( '#  ' + Menu.DATE.strftime('%m/%d/%Y') + ' #' )
		print( '###############' )
		print()
		print( 'Select Day' )

		sel = Menu.show_menu(options)
		Menu.obs['day'] = options[sel][0]

		return options[sel][1]()
		
	
	def ini_menu():
		print( '###############' )
		print( '# {haz} -{sec}- #'.format(haz=Menu.obs['haz'][0], sec=Menu.obs['sec']) )
		print( '#  ' + Menu.obs['day'] + ' #' )
		print( '###############' )
		print()
		print( 'Select Initial Time' )
		
		Menu.obs['ini'] = input('\n>> ')
		
		return Menu.get_obs()
		
		
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
		# build options specific for EURO/CMC and GFS/NAM
		options = {}
		if Menu.mdl['mdl']=='EURO' or Menu.mdl['mdl']=='CMC':
			options = {'1':('00Z',Menu.mdl_sauc),
					   '2':('12Z',Menu.mdl_sauc)}
		else:
			options = {'1':('00Z',Menu.mdl_sauc),
					   '2':('06Z',Menu.mdl_sauc),
					   '3':('12Z',Menu.mdl_sauc),
					   '4':('18Z',Menu.mdl_sauc)}
		
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