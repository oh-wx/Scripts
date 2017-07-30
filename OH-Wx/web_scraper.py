import os
import sys

import urllib.request
from bs4 import BeautifulSoup
import requests

#page = urllib.request.urlopen('http://mp1.met.psu.edu/~fxg1/ECMWF_0z/ecmwfloop.html').read()
#soup = BeautifulSoup(page, 'html.parser')

#imgs = soup.findAll('a', {'href': '#picture'})
#print( 'Num of imgs:  ' + str(len(imgs)) )
#print( imgs[0]['src'] )

repository = 'C:\Storm_Images\Test\python'


# need to implement EURO past 168hrs;  url = .../ECMWF0.5_{init}/...
def psu_data(model, init):
	os.system('cls')
	models = {'EURO':('ECMWF_','ECMWF0.5_'), 'CMC':('CMC_','CMCNA_'), 'GFS':'MRF_'}
	interval = 12
	
	print( '### {init} {mdl} Selected ###'.format(init=init, mdl=model) )
	print()
	start = int( input('Starting hour >>  ') )
	stop  = int( input('Ending hour   >>  ') )
	
	if model == 'CMC':
		if init == '12z':
			url = models[model][1] + init
		else:
			url = models[model][0] + init
	else:
		url = models[model] + init

	if model == 'EURO':
		interval = 24

	print()
	
	for i in range(start, stop+interval, interval):
		if i == 0:
			i = '00'
		image = 'http://mp1.met.psu.edu/~fxg1/{model}/f{hr}.gif'.format(hr=i, model=url)
		fyle = '{hr}hr_{model}-{init}Z.gif'.format( hr=i, model=model, init=init.strip('z') )
		write_file(image, fyle)
		
		print(fyle)
		
		#with open(fyle, 'wb') as f:
			#f.write( requests.get(image).content )

def twd_data(model, init):
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
	
	levels = ['10', '925', '850', '700', '500', '300']
	param  = ['WSPD', 'TMPF']
	
	image = 'http://www.twisterdata.com/data/models/gfs/3/maps/2016/12/19/06/GFS_3_2016121906_F120_TMPF_2_M_ABOVE_GROUND.png'
	fyle = repository + '/test.png'

	with open(fyle, 'wb') as f:
		f.write( requests.get(image).content )
		
	'''
	
	print( '### TEST ###' )
	print( 'TwisterData has not been implemented' )
	print( str(model) + ' ' + str(init) )

def spc_meso():
#################	#################################################################################################
#	Sectors		#	#										Severe													#
#	NE - s16	#	#																								#
#	EC - s17	#	# surface:	obs 		winds:	925mb	therm:	SBCAPE	shear:	EFF SHR		comp:	SCCOMP		#
#	MW - s20	#	#			pressure			850mb			MLCAPE			6Km					SIGTOR		#
#	US - s19	#	#			temp/dewpt			700mb			MUCAPE			8Km					1Km EHI		#
#################	#			div/vort			500mb			MLR				1Km					3Km EHI		#
					#								300mb			LLR				EFF SRH				DERCHO ???	#
					#			VISSAT				H5 Vort			LCL				1Km SRH							#
					#			RDR					H3 Circ							3Km SRH							#
					#																9-11Km							#
					#################################################################################################

					#############################################################
					#							Winter							#
					# surface:	obs		winds:	925mb		winter:	sfc temp	#
					#			pressure		850mb				sfc bulb	#
					#			temp/dewpt		700mb				max bulb	#
					#							500mb							#
					#			VISSAT			300mb							#
					#			RDR				H5 Vort							#
					#							H3 Circ							#
					#############################################################

	### URL:  http://www.spc.noaa.gov/exper/mesoanalysis/{sector}/{param}/{param}.gif ## NOTE: for filled colors {param}_sf.gif  ###
	
	### ONLY CURRENT OBS IMPLEMENTED ###
	### Errors with initial time, need to determine when the new data becomes available after the hour ###
	
	
	# retrieve and format time and date
	page = urllib.request.urlopen('http://www.spc.noaa.gov/exper/mesoanalysis/new/viewsector.php?sector=20').read()
	datetime = str( BeautifulSoup(page, 'html.parser').findAll('div', {'id': 'latest'})[0].text ).split( )
	init = str( datetime[1] )
	date = datetime[0].split('/')
	date = str( '20'+date[2]+date[0]+date[1] )
	
	sector  = {1:('s16','NE'), 2:('s17','EC'), 3:('s20','MW'), 4:('s19','US')}
	
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
	
	severe  = (surface, winds, thermo, shear, comp)
	winter  = (surface, winds, frozen)
	menu 	= {1:severe, 2:winter}
	
	print( '### SPC Meso-analsys ###' )
	print()
	print( 'Select Hazard Type' )
	print( '1. Severe' )
	print( '2. Winter' )
	
	hazard = menu[int(input('\n>> '))]
	os.system('cls')
	
	# ugly way to determine Hazard Type
	print( '### {haz} Wx Selected ~{time}Z - {date} ###'.format(haz='Severe' if len(hazard)>3 else 'Winter', time=init, date=date) )
	print()
	print( 'Select Sector' )
	print( '1. NE' )
	print( '2. EC' )
	print( '3. MW' )
	print( '4. US' )
	
	sect = sector[int(input('\n>> '))]
	
	for i in range(len(hazard)):
		for n in range(len(hazard[i])):
			# less ugly conditional for filled color images
			if len(hazard[i][n]) == 3:
				url  = 'http://www.spc.noaa.gov/exper/mesoanalysis/{sector}/{param}/{param}_sf.gif'.format(sector=sect[0], param=hazard[i][n][1])
			else:
				url  = 'http://www.spc.noaa.gov/exper/mesoanalysis/{sector}/{param}/{param}.gif'.format(sector=sect[0], param=hazard[i][n][1])
				
			fyle = hazard[i][n][0] + '~{init}Z-'.format(init=init) + sect[1] + '-{date}.gif'.format(date=date)
			write_file(url, fyle)
			print(fyle)
	
	#print( '1. Current Obs' )
	#print( '2. Past Obs' )
	
	
					
def write_file(url, fyle):
	global repository
	
	path = repository + '/' + fyle
	with open(path, 'wb') as f:
			f.write( requests.get(url).content )
					
	
def mdl_menu():
	os.system('cls')
	
	models  = {1:'EURO', 2:'CMC', 3:'GFS', 4:'NAM', 5:'RAP'}
	init    = {1:('0z', '12z'), 2:('0z','6z','12z','18z')}
	
	print( 'Select a model:' )
	print( '1. EURO' )
	print( '2. CMC' )
	print( '3. GFS' )
	print( '4. NAM' )
	print( '5. RAP' )
	print( '9. Back' )
	
	model = int( input('\n>> ') )	# keep as index for initial time logic
	os.system('cls')

	print( '### {mdl} Selected ###'.format(mdl=models[model]) )
	print()
	# RAP model can take 'any' initial time
	if model == 5:
		init = str( input( 'Enter an initial time:  ' ) ) + 'Z'
	# otherwise standard initial time required
	else:
		print( 'Enter an initial time:' )
		# determine list of initial time from model input and print; +1 for human readability
		for i in range( len(init[1]) ) if model<3 else range( len(init[2]) ):
			print( '{i}. {init}'.format(i=i+1, init = init[1][i] if model<3 else init[2][i]) )
			
		# determine initial time from appropriate list; -1 from human readability
		init = init[1][int( input('\n>> ') )-1] if model<3 else init[2][int( input('\n>> ') )-1]
	os.system('cls')
	
	# GFS has two potential sources
	if model == 3:
		print( '### {init} {mdl} Selected ###'.format(init=init, mdl=models[model]) )
		print()
		print( 'Select a distribution:' )
		print( '1. Penn St EWALL' )
		print( '2. Twister Data' )
		
		# determine GFS source
		psu_data( models[model], init) if int(input('\n>> '))==1 else twd_data( models[model], init)
	elif model < 3:
		psu_data( models[model], init)
	else:
		twd_data( models[model], init)

	
def main_menu():
	os.system('cls')
	
	print( '##################' )
	print( '# Wx Data Gather #' )
	print( '##################' )
	print()
	print( 'Select Wx Data:' )
	print( '1. Observations' )
	print( '2. Models' )
	print( '0. Exit' )
	
	exec_menu( input('\n>> ') )
	
	
def exec_menu(choice):
	os.system('cls')
	
	actions = {
		'main':main_menu,
		'1':spc_meso,
		'2':mdl_menu,
		'0':exit}		
	ch = choice.lower()
	
	if ch == '':
		actions['main']()
	else:
		try:
			actions[ch]()
		except KeyError:
			# implement menu stack for back() ???
			print( 'Invalid selection' )
			actions['main']()

			
def play():
	os.system('cls')
	
	'''
	wx_data = {1:'Current Obs', 2:'Past Obs (3-days)', 3:'Models'}
	models  = {1:'EURO', 2:'CMC', 3:'GFS', 4:'NAM', 5:'RAP'}
	init    = {1:('0z', '12z'), 2:('0z','6z','12z','18z')}
	
	print( '##################' )
	print( '# Wx Data Gather #' )
	print( '##################' )
	print()
	print( 'Select Wx Data:' )
	for k,d in wx_data.items():
		print( str(k) + '. ' + d )
	if int( input() ) < 3:
		spc_meso()
	
	print( 'Select a model:' )
	for k,m in models.items():
		print( str(k) + '. ' + m )
	
	model = int( input() )	# keep as index for initial time logic
	os.system('cls')

	print( '### {mdl} Selected ###'.format(mdl=models[model]) )
	print()
	if model == 5:
		init = str( input( 'Enter an initial time:  ' ) ) + 'Z'
	else:
		print( 'Enter an initial time:' )
		for i in range( len(init[1]) ) if model<3 else range( len(init[2]) ):
			print( '{i}. {init}'.format(i=i+1, init = init[1][i] if model<3 else init[2][i]) )
		
		init = init[1][int( input() )-1] if model<3 else init[2][int( input() )-1]
	os.system('cls')
	
	if model == 3:
		print( '### {init} {mdl} Selected ###'.format(init=init, mdl=models[model]) )
		print()
		print( 'Select a distribution:' )
		print( '1. Penn St EWALL' )
		print( '2. Twister Data' )
		
		psu_data( models[model], init) if int(input())==1 else twd_data( models[model], init)
	elif model < 3:
		psu_data( models[model], init)
	else:
		twd_data( models[model], init)
	'''
		
def main():
	
	#site  = input('Gather model data from PSU or TD?')
	#init  = input('Initial time (00Z, 06Z, 12Z, or 18Z)?').upper()
	#model = input('GFS, EURO, NAM, RAP?').upper()
	
	#play()
	main_menu()
	print('\nComplete\n')
	
main()
	
