import os
import sys

import urllib.request
from bs4 import BeautifulSoup
import requests
import datetime
from datetime import date, timedelta


### TO-DO ###
#
#	implement get_twd(), get_cod()
#
#	
#	update Obs Menu Titles for hazard type
#
#	implement grab_data()
#		unify data struct for obs and mdl



class Menu:
	### GLOBALS ###
	REPO = 'C:\\Users\\anwalters\\Desktop\\OH-Wx\\DataGrab\\'
	DATE = None
	
	page = None
	init = None
	date = None
	
	obs = None
	mdl = None
	stack = None
	
	# initialize all variables, set init and date as default, clean stack
	def __init__(self):
		# get init time and format date for Current Obs
		Menu.DATE = datetime.datetime.now()
		Menu.page = urllib.request.urlopen('http://www.spc.noaa.gov/exper/mesoanalysis/new/viewsector.php?sector=20').read()
		Menu.init = str( BeautifulSoup(page, 'html.parser').findAll('div', {'id': 'latest'})[0].text ).split()[1]
		Menu.date = DATE.strftime('%Y%m%d')
		
		
		Menu.obs = {'haz':None, 'sec':None, 'day':Menu.date, 'ini':Menu.init}
		Menu.mdl = {'mdl':None, 'ini':None, 'src':None}
		Menu.stack =[]

	
	
	''' Potential expansion
	def grab_data(start, stop, interval, url):
		i = Menu.obs['ini'].split('-')
		if len(i) > 1:
			for n in range(int(i[0]),int(i[1])+1):
				Menu.obs['ini'] = str(n)
				Menu.get_obs()
		else:
			Menu.obs['ini'] = i[0]
			return Menu.get_obs()
	'''
		
	
	def write_file(url, fyle):
		path = Menu.REPO + Menu.obs['ini'] +'Z/'
		
		if Menu.obs['ini'] == '':
			path = Menu.REPO + Menu.init + 'Z/'

		if not os.path.exists(path):
			os.makedirs(path)
		
		path = path + fyle
		with open(path, 'wb') as f:
				f.write( requests.get(url).content )		
		print(fyle)
		
	
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
		### PastOBS:http://www.spc.noaa.gov/exper/mesoanalysis/{sector}/{param}/sfc_{date}_{init}00.gif
		### Rdr :	http://www.spc.noaa.gov/exper/mesoanalysis/{sector}/rgnlrad/rgnlrad.gif
		### Vis :	http://www.spc.noaa.gov/exper/mesoanalysis/{sector}/1kmv/1kmv.gif
		### Arch:	http://www.spc.noaa.gov/exper/ma_archive/images_s4/{yyyymmdd}/{init}_{param}.gif

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
				   ('H3CIRC','ageo',True),
				   ('H8FRNT','8fnt',True),
				   ('H7FRNT','7fnt',True),
				   ('H8TADV','tadv',True),
				   ('H7TADV','7tad',True),
				   ('HGHCHG','500mb_chg',True),
				   ('H3VORT','padv',True)]
				   
		thermo  = [('SBCAPE','sbcp',True),
				   ('MLCAPE','mlcp',True),
				   ('MUCAPE','mucp',True),
				   ('MLR','laps',True),
				   ('LLR','lllr',True),
				   ('LCL','lclh',True),
				   ('LFC','lfch',True),
				   ('MIX','mxth',True)]
				   
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
		sector  = {'SP':'s15','NE':'s16','EC':'s17','SE':'s18','US':'s19','MW':'s20','CP':'s14'}
		hazard	= {'1':severe,
				   '2':winter,
				   'D':('DERCHO','dcp'),
				   'P':('PWAT','pwtr',True),
				   'M':('MCSPRB','mcsm'),
				   'H':('HAIL','hail'),
				   'R':('BR','rgnlrad'),
				   'V':('VISSAT','1kmv'),
				   'I':('MLRDEW','tdlr',True),
				   'L':('MAXLR','maxlr'),
				   'T':('H8TRAN','tran',True),
				   'O':('CRSOVR','comp',True),
				   'S':('STRECH','desp'),
				   'A':('CANGLE','crit'),
				   'C':('H8CONV','ddiv',True)}
		
		# get obs data to build URL
		sector = sector[Menu.obs['sec']]
		current = True if Menu.obs['ini'] == '' else False
		archive = True if (Menu.DATE - Menu.obs['day']).total_seconds() > 432000 else False
		past = Menu.obs['day'].strftime('%y%m%d')
		formdate = Menu.obs['day'].strftime('%Y%m%d')
		parameter = []
		popped = False
		
		if not Menu.obs['ini']=='':
			Menu.obs['ini'] = Menu.obs['ini'].zfill(2)		# zero fill init
		
		
		# build parameter list
		if Menu.obs['haz'][0]=='1' or Menu.obs['haz'][0]=='2':
			parameter = hazard[Menu.obs['haz'][0]]		# assign default list to parameter for append below
			popped = True								
		
		# if default list exists from above, skip it
		for item in Menu.obs['haz'][1:] if popped else Menu.obs['haz']:
			parameter.append(hazard[item])

		# grab data!
		for i in range(len(parameter)):
			if archive:
				url = 'http://www.spc.noaa.gov/exper/ma_archive/images_s4/{date}/{init}_{param}'.format(date=formdate, init=Menu.obs['ini'], param=parameter[i][1])
			else:
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
			
			fyle = parameter[i][0] + '~{init}Z-'.format(init=Menu.init if Menu.obs['ini'] ==  '' else Menu.obs['ini']) + Menu.obs['sec'] + '-' + formdate + '.gif'
			Menu.write_file(url, fyle)
		
	# --------- end get_obs() ---------- #
	
	def get_psu():
		banner = ''
		banner = banner.ljust(len(Menu.mdl['mdl'])+4,'#')
		print( banner ) #if Menu.mdl['mdl']=='EURO' else print( '############' )	# stupid formatting conditionals
		print( '# {mdl} ~{init} #'.format(mdl=Menu.mdl['mdl'], init=Menu.mdl['ini']) )
		print( banner ) #if Menu.mdl['mdl']=='EURO' else print( '############' )	# stupid formatting conditionals
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
			
			if model=='EURO': #and i>168:						# < ------------ ERROR @ PSU model[0] url broken
				url = models[model][1] + init					# < ------------ ||

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
			  
			  'http://www.twisterdata.com/data/models/nam/221/maps/{yyyy}/{mm}/{dd}/{ii}/NAM_221_{yyyymmddii}_F{hr}_{param}_{level}.png'
			  'http://www.twisterdata.com/data/models/gfs/3/maps/{yyyy}/{mm}/{dd}/{ii}/GFS_3_{yyyymmddii}_F{hr}_{param}_{level}.png'
			  'http://www.twisterdata.com/data/models/rap/255/maps/{yyyy}/{mm}/{dd}/{ii}/RAP_255_{yyyymmddii}_F{hr}_{param}_{level}.png'
		
		
		 NOTES:  levels are a little finicky
					SRM 				- '6000_M'
					RAP EHI/SRH/PWAT/LCL- 'SURFACE'
					LIFT 				- '500_1000_MB'
					MAXTEMP 			- 'SFC_500MB'
					NAM SRH				- '3000_M_ABOVE_GROUND_0_M_ABOVE_GROUND'
					NAM EHI				- '3000_M'
					
				GFS does not offer SRH maps
		'''
	
		# winds use 10M ABOVE GROUND, temp/dewpt use 2M ABOVE GROUND
		model	= {'GFS':('gfs','3','GFS_3_'),
				   'NAM':('nam','221','NAM_221_'),
				   'RAP':('rap','255','RAP_255_')}
				   
		'''
		level	= [('SFC','2_M_ABOVE_GROUND','10_M_ABOVE_GROUND','SURFACE'),
				   ('925mb','925_MB'),
				   ('850mb','850_MB'),
				   ('700mb','700_MB'),
				   ('500mb','500_MB'),
				   ('300mb','300_MB')]
		
		petig	= [('WIND','WSPD'),
				   ('TEMP','TMPF','TMPC'),
				   ('DEWPT','DPTF','DPTC'),
				   ('700mbRH','RH_700_MB'),
				   ('PWAT','PWATIN_SURFACE')]
		'''
				   
		winds	= [('SFC_WIND','10_M_ABOVE_GROUND_WSPD'),
				   ('925mbWIND','925_MB_WSPD'),
				   ('850mbWIND','850_MB_WSPD'),
				   ('700mbWIND','700_MB_WSPD'),
				   ('500mbWIND','500_MB_WSPD'),
				   ('300mbWIND','300_MB_WSPD')]
				   
		temps	= [('SFC_TEMP','2_M_ABOVE_GROUND_TMPF'),
				   ('925mbTEMP','925_MB_TMPC'),
				   ('850mbTEMP','850_MB_TMPC')]
				   
		dewpt	= [('SFC_DEWP','2_M_ABOVE_GROUND_DPTF'),
				   ('925mbDEWP','925_MB_DPTC'),
				   ('850mbDEWP','850_MB_DPTC'),
				   ('700mbRH','RH_700_MB'),
				   ('PWAT','PWATIN_SURFACE')]
				  
		therm	= [('CAPE','CAPE_SURFACE'),
				   ('CIN','CIN_SURFACE'),
				   ('LCL','ZLCLM_SURFACE')]
				   #('LIFT','LFTX_')]
		
		helcy	= [('1KmEHI','EHI1_SURFACE','EHI_1000_M'),
				   ('3KmEHI','EHI3_SURFACE','EHI_3000_M'),
				   ('1KmSRH','HLCY1_SURFACE','HLCY_1000_M_ABOVE_GROUND_0_M_ABOVE_GROUND'),
				   ('3KmSRH','HLCY3_SURFACE','HLCY_3000_M_ABOVE_GROUND_0_M_ABOVE_GROUND')]
				   
		shear	= [('VORT','RELV_500_MB'),
				   ('500mbSHR','SHRM_500_MB'),
				   ('MOTION','SSPD_6000_M')]
				   
		wintr	= [('MAXTEMP','TVMXC_SURFACE_500_MB')]
				   
		
		severe = (winds, temps[0], dewpt, therm, shear) if Menu.mdl['mdl']=='GFS' else (winds, temps[0], dewpt, therm, shear, helcy)
		winter = (temps, dewpt, wintr)
				  
		#formdate = 
		
		print( '### TEST ###' )
		print( 'TwisterData has not been implemented' )
		print( str(model) + ' ' + str(init) )
		# --------- end get_twd() ---------- #
	
	'''
	def get_iwx():
		banner = ''
		banner = banner.ljust(len(Menu.mdl['mdl'])+4,'#')
		print( banner ) #if Menu.mdl['mdl']=='EURO' else print( '############' )	# stupid formatting conditionals
		print( '# Instant Wx Maps - {mdl} ~{init} #'.format(mdl=Menu.mdl['mdl'], init=Menu.mdl['ini']) )
		print( banner ) #if Menu.mdl['mdl']=='EURO' else print( '############' )	# stupid formatting conditionals
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
			
			if model=='EURO': #and i>168:						# < ------------ ERROR @ PSU model[0] url broken
				url = models[model][1] + init	*/				# < ------------ ||
		
		image = 'http://www.instantweathermaps.com/ECMWF/2017121812/USA_PRMSL_msl_144.gif'	#.format(hr=i, model=url)
		fyle = 'test.gif'	#.format( hr=i, model=model, init=init.strip('z').zfill(2) ) + Menu.DATE.strftime('%Y%m%d') + '.gif'
		Menu.write_file(image, fyle) 
	'''
		
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
		options = ['1','2','9','R','V','P','C','H','M','D','L','I','T','O','S', 'A']
				   
		print( '#########################' )
		print( '#     Observations      #' )
		print( '#                       #' )
		print( '# Additional Parameters #' )
		print( '# R: Base Reflectivity  #' )
		print( '# V: Visible Satellite  #' )
		print( '# P: Precipitable Water #' )
		print( '# H: Hail Parameters	#' )
		print( '# M: MCS Maintenance	#' )
		print( '# D: Derecho Composite  #' )
		print( '# L: Max Lapse Rate     #' )
		print( '# I: Mid LR & Sfc Dewpt #' )
		print( '# T: 850mb Moist Trans  #' )
		print( '# O: H8-H5 Cross Over   #' )
		print( '# S: Low Level Stretch  #' )
		print( '# A: Critical Angle     #' )
		print( '# C: 850mb Convergence  #' )
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
			Menu.stack.append(Menu.haz_menu)
			os.system('cls')
			return Menu.haz_menu()
		
	### bad formatting with new hazard value ###
	def haz_menu():
		options = {'1':('MW',Menu.day_menu),
				   '2':('EC',Menu.day_menu),
				   '3':('CP',Menu.day_menu),
				   '4':('NE',Menu.day_menu),
				   '5':('US',Menu.day_menu),
				   '6':('SP',Menu.day_menu),
				   '7':('SE',Menu.day_menu),
				   '9':('Back',Menu.back)}

		print( '#############' )
		print( '# {haz} Wx #'.format(haz='Winter' if Menu.obs['haz'][0]=='2' else 'Severe') )
		print( '#############' )
		print()
		print( 'Select Sector' )

		sel = Menu.show_menu(options)
		Menu.obs['sec'] = options[sel][0]
				
		return options[sel][1]()
		

	### bad formatting with new hazard value ###
	def day_menu():
		options = {'1':('Today',Menu.ini_menu)}
		# add 4 prior days to options		   
		for i in range(1,5):
			formdate = Menu.DATE + timedelta(days = -i)
			options[str(i+1)] = (formdate.strftime('%m/%d/%Y'),Menu.ini_menu)		
		options['6'] = ('Archive', Menu.ini_menu)
		options['9'] = ('Back', Menu.back)

		print( '###############' )
		print( '# {haz} -{sec}- #'.format(haz='Winter' if Menu.obs['haz'][0]=='2' else 'Severe', sec=Menu.obs['sec']) )
		print( '#  ' + Menu.DATE.strftime('%m/%d/%Y') + ' #' )
		print( '###############' )
		print()
		print( 'Select Day' )

		sel = Menu.show_menu(options)
		
		# if archive day selected, get date
		if sel == '6':
			print( '\nEnter the Archive date (mm/dd/yyyy):' )
			date = input('\n>> ')
			date = date.split('/')
			Menu.obs['day'] = datetime.datetime(int(date[2]),int(date[0]),int(date[1]))
		else:
			Menu.obs['day'] = Menu.DATE + timedelta(days = -(int(sel)-1))

		return options[sel][1]()
		
	
	def ini_menu():
		print( '###############' )
		print( '# {haz} -{sec}- #'.format(haz='Winter' if Menu.obs['haz'][0]=='2' else 'Severe', sec=Menu.obs['sec']) )
		print( '#  ' + Menu.obs['day'].strftime('%m/%d/%Y') + ' #' )
		print( '###############' )
		print()
		print( '9. Back\n' )
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
		banner = ''
		banner = banner.ljust(len(Menu.mdl['mdl'])+4,'#')

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
		
		print( banner )# if Menu.mdl['mdl']=='EURO' else print( '#######' )	# stupid formatting conditionals
		print( '# {mdl} #'.format(mdl=Menu.mdl['mdl']) ) 
		print( banner )# if Menu.mdl['mdl']=='EURO' else print( '#######' )	# stupid formatting conditionals
		print()
		
		sel = Menu.show_menu(options)
		Menu.mdl['ini'] = options[sel][0]
		
		return options[sel][1]()
	
	
	def mdl_sauc():
		options = {'1':('PSU Ewall',  Menu.get_psu),
				   '2':('Twisterdata',Menu.get_twd)}
				   #'3':('Inst Wx Map',Menu.get_iwx)}
		
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

	while(True):
		Menu()
		Menu.main_menu()
		print('\nData Grab Complete')
		input('\nPress Enter\n')
		
		
	
main()