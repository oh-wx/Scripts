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

	REPO = 'C:\\Storm_Images\\NEW---TEMP\\DataGrab\\'
	DATE = None
	
	page = None
	init = None
	date = None
	SPCdate = None
	archive = None
	
	obs = None
	stack = None
	
	# initialize all variables, set init and date as default, clean stack
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
		path = Menu.REPO + Menu.obs['ini'] +'Z' + Menu.obs['day'].strftime('%d') + '/'
		
		if Menu.obs['ini'] == '':
			path = Menu.REPO + Menu.init + 'Z' + Menu.obs['day'].strftime('%d') + '/'

		if not os.path.exists(path):
			os.makedirs(path)
		
		path = path + fyle
		with open(path, 'wb') as f:
			try:
				f.write( requests.get(url).content )
			except urllib.URLError:
				print( "Could not download: " + fyle )
				return
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
			
	def get_goes16(lat, lon):
		### Centered OKC:	"https://weather.msfc.nasa.gov/cgi-bin/get-abi?satellite=GOESEastconusband02&lat=35&lon=-97&zoom=1&width=1400&height=1000&quality=100"
		### Centered DFW:	"https://weather.msfc.nasa.gov/cgi-bin/get-abi?satellite=GOESEastconusband02&lat=32&lon=-96&zoom=1&width=1400&height=1000&quality=100"
		### Centered CHL:	"https://weather.msfc.nasa.gov/cgi-bin/get-abi?satellite=GOESEastconusband02&lat=34&lon=-100&zoom=1&width=1400&height=1000&quality=100"
		### Centered WDW:	"https://weather.msfc.nasa.gov/cgi-bin/get-abi?satellite=GOESEastconusband02&lat=36&lon=-99&zoom=1&width=1400&height=1000&quality=100"
		### Centered WTC:	"https://weather.msfc.nasa.gov/cgi-bin/get-abi?satellite=GOESEastconusband02&lat=37&lon=-97&zoom=1&width=1400&height=1000&quality=100"

		curt = datetime.datetime.now() + timedelta(minutes =- 4)	# image is being captured 4min after valid
		api_url = "https://weather.msfc.nasa.gov/cgi-bin/get-abi?satellite=GOESEastconusband02&lat={lat}&lon={lon}&zoom=1&width=1400&height=1000&quality=100"\
				  .format(lat=lat, lon=lon)
		
		page = urllib.request.urlopen(api_url).read()
		images = BeautifulSoup(page, 'html.parser').findAll('img')
		
		url = "https://weather.msfc.nasa.gov" + images[0]['src']
		fyle = "VISSAT~" + curt.strftime('%H') + curt.strftime('%M') + "-GOES16-" + curt.strftime('%Y%m%d') + ".gif"
		
		Menu.write_file(url, fyle)
		
	def get_mesonet(sec):
		### S. Plains:	"http://rain.ttu.edu/sfc_plots/L_SPLNS_plot.gif"
		### Texas:		"http://rain.ttu.edu/sfc_plots/L_txplot.gif"
		### W. Texas:	"http://rain.ttu.edu/sfc_plots/L_sjt_plot.gif"
		### TX Phandle:	"http://rain.ttu.edu/sfc_plots/L_LBB_plot.gif"
		### OK Mesonet:	"http://www.mesonet.org/data/public/mesonet/maps/realtime/current.wx.gif"
		
		sectors	= {'SPL':'http://rain.ttu.edu/sfc_plots/L_SPLNS_plot.gif',
				   'TX':'http://rain.ttu.edu/sfc_plots/L_txplot.gif',
				   'WTX':'http://rain.ttu.edu/sfc_plots/L_sjt_plot.gif',
				   'TXP':'http://rain.ttu.edu/sfc_plots/L_LBB_plot.gif',
				   'OK':'http://www.mesonet.org/data/public/mesonet/maps/realtime/current.wx.gif',
				   'CPL':'http://rain.ttu.edu/sfc_plots/L_cen_usplot.gif',
				   'FWD':'http://rain.ttu.edu/sfc_plots/L_dfw.gif',
				   'TXP':'http://rain.ttu.edu/sfc_plots/L_PAN_plot.gif'}
				   
		for s in sec:
			fyle = "OBS~" + Menu.init + "Z-" + s + "-" + Menu.obs['day'].strftime('%Y%m%d') + ".gif"
			Menu.write_file( sectors[s], fyle )
		
	
	def get_obs():
		### Curr:	http://www.spc.noaa.gov/exper/mesoanalysis/{sector}/{param}/{param}.gif					## NOTE: for filled colors {param}_sf.gif
		### Past:	http://www.spc.noaa.gov/exper/mesoanalysis/{sector}/{param}/{param}_{date}{init}.gif	## NOTE: oldest image is -4 days to the init
		### PastOBS:http://www.spc.noaa.gov/exper/mesoanalysis/{sector}/{param}/sfc_{date}_{init}00.gif
		### Rdr :	http://www.spc.noaa.gov/exper/mesoanalysis/{sector}/rgnlrad/rgnlrad.gif
		### Vis :	http://www.spc.noaa.gov/exper/mesoanalysis/{sector}/1kmv/1kmv.gif
		### Arch:	http://www.spc.noaa.gov/exper/ma_archive/images_s4/{yyyymmdd}/{init}_{param}.gif

		# atmospheric parameter groups
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
				   ('HGHCHG','500mb_chg'),
				   ('H3VORT','padv',True),
				   ('MSTRCN','mcon'),
				   ('H8TRAN','tran',True),
				   ('H9TRAN','tran_925',True),
				   ('H9FRNT','9fnt'),
				   ('H9TADV','tadv_925',True),
				   ('SBFRNT','sfnt'),
				   ('H8WIND','850mb2')]
				   
		thermo  = [('SBCAPE','sbcp',True),
				   ('MLCAPE','mlcp',True),
				   ('MUCAPE','mucp',True),
				   ('SBLI','muli',True),
				   ('MLR','laps',True),
				   ('LLR','lllr',True),
				   ('LCL','lclh',True),
				   ('LFC','lfch',True),
				   ('MIX','mxth',True),
				   ('THETAE','thea',True),
				   ('MIXAVG','mixr',True),
				   ('3CAPE','lr3c',True),
				   ('3KmC&V','3cvr'),
				   ('DCAPE','dcape')]
				   
		shear	= [('6KmSHR','shr6'),
				   ('8KmSHR','shr8'),
				   ('1KmSHR','shr1'),
				   ('EFFSHR','eshr'),
				   ('EFFSRH','effh'),
				   ('3KmSRH','srh3'),
				   ('1KmSRH','srh1'),
				   ('9-11KmSRW','ulsr'),
				   ('AVLSRW','alsr'),
				   ('SBVORT','dvvr',True),
				   ('3KmSHR','shr3')]
				   
		comp	= [('SCCOMP','scp'),
				   ('SIGTOR','stpc'),
				   ('1KmEHI','ehi1'),
				   ('3KmEHI','ehi3')]
				   
		frozen	= [('SFCTEMP','fztp'),
				   ('SFCBULB','swbt'),
				   ('MAXBULB','mxwb')]
				  
		severe  = thermo + shear + comp
		winter  = frozen
		
		# dictionaries for Obs Menu selection
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
				   'O':('CRSOVR','comp',True),
				   'S':('STRECH','desp'),
				   'A':('CANGLE','crit'),
				   'C':('H8CONV','ddiv',True),
				   'E':('MLCSHR','mlcp_eshr',True)}
		
		# get obs data to build URL
		current = True if Menu.obs['ini'] == '' else False
		#archive = True if (Menu.DATE - Menu.obs['day']).total_seconds() > 432000 else False
		past = Menu.obs['day'].strftime('%y%m%d')
		formdate = Menu.obs['day'].strftime('%Y%m%d')
		parameter = petig	# assign petigre data as default params
		
		if not Menu.obs['ini']=='':
			Menu.obs['ini'] = Menu.obs['ini'].zfill(2)		# zero fill init

		# build parameter list
		for item in Menu.obs['haz']:
			# issues concating tuple list and dictionary tuple
			if item=='1' or item=='2':
				parameter += hazard[item]
			else:
				parameter.append( hazard[item] )
			
		# grab data!
		for s in Menu.obs['sec']:
			for i in range(len(parameter)):
				if Menu.archive:
					url = 'http://www.spc.noaa.gov/exper/ma_archive/images_s4/{date}/{init}_{param}'.format(date=formdate, init=Menu.obs['ini'], param=parameter[i][1])
				else:
					url = 'http://www.spc.noaa.gov/exper/mesoanalysis/{sector}/{param}/'.format(sector=s[1], param=parameter[i][1])
				
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
				
				fyle = parameter[i][0] + '~{init}Z-'.format(init=Menu.init if Menu.obs['ini'] ==  '' else Menu.obs['ini']) + s[0] + '-' + formdate + '.gif'
				Menu.write_file(url, fyle)
		
	# --------- end get_obs() ---------- #
	
	def main_menu():
		options = {'1':('Observations',Menu.obs_menu),
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
		options = ['1','2','9','R','V','P','C','H','M','D','L','I','O','S', 'A', 'E']
				   
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
		print( '# O: H8-H5 Cross Over   #' )
		print( '# S: Low Level Stretch  #' )
		print( '# A: Critical Angle     #' )
		print( '# C: 850mb Convergence  #' )
		print( '# E: Eff Shr & MLCAPE   #' )
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
				   
		sector  = {'SP':['SP','s15'],
				   'NE':['NE','s16'],
				   'EC':['EC','s17'],
				   'SE':['SE','s18'],
				   'US':['US','s19'],
				   'MW':['MW','s20'],
				   'CP':['CP','s14'],
				   'NP':['NP','s13'],
				   'SW':['SW','s12']}
		sectors = []

		print( '#############' )
		print( '# {haz} Wx #'.format(haz='Winter' if Menu.obs['haz'][0]=='2' else 'Severe') )
		print( '#############' )
		print()
		print( 'Select Sector' )
		print( 'For multiple Sectors separate by a space' )
		print()
		print( '####################' )
		print( '#     Sectors      #' )
		print( '#                  #' )
		print( '# Midwest   - MW   #' )
		print( '# S. Plains - SP   #' )
		print( '# U.S.      - US   #' )
		print( '# C. Plains - CP   #' )
		print( '# Northeast - NE   #' )
		print( '# Southeast - SE   #' )
		print( '# E. Coast  - EC   #' )
		print( '# N. Plains - NP   #' )
		print( '# Southwest - SW   #' )
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
		for i in range(1,5):
			formdate = Menu.DATE + timedelta(days = -i)
			options[str(i+1)] = (formdate.strftime('%m/%d/%Y'),Menu.ini_menu)		
		options['6'] = ('Archive', Menu.ini_menu)
		options['9'] = ('Back', Menu.back)

		print( '###############' )
		print( '# {haz} -{sec}- #'.format(haz='Winter' if Menu.obs['haz'][0]=='2' else 'Severe', sec=Menu.obs['sec'][0]) )
		print( '#  ' + Menu.DATE.strftime('%m/%d/%Y') + ' #' )
		print( '###############' )
		print()
		print( 'Select Day' )

		sel = Menu.show_menu(options)
		
		# if archive day selected, get date
		if sel == '6':
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
		satlat = 33
		satlon = -97.3
		sectors = ['TX','OK','SPL','FWD','TXP']	# array of MesoNet sector(s)

		
				   
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
						Menu.get_mesonet(sectors)
						Menu.get_goes16(satlat,satlon)
						
						time.sleep(65)	# only grab obs once per hour
					
					if( (curt.minute%5) == 0 ):
						Menu.get_goes16(satlat, satlon)
						time.sleep(65)	# only grab goes16 once per 5min
					
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

		
	
		
def main():

	while(True):
		Menu()
		Menu.main_menu()
		print('\nData Grab Complete')
		input('\nPress Enter\n')
		
		
	
main()