import os
import sys

import urllib.request
from bs4 import BeautifulSoup
import requests
import datetime
from datetime import date, timedelta
import time


class Write:
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
		Write.page = urllib.request.urlopen('http://www.spc.noaa.gov/exper/mesoanalysis/new/viewsector.php?sector=20').read()
		Write.init = str( BeautifulSoup(Write.page, 'html.parser').findAll('div', {'id': 'latest'})[0].text ).split()[1]
		Write.archive = False
		
		Write.SPCdate = str( BeautifulSoup(Write.page, 'html.parser').findAll('div', {'id': 'latest'})[0].text ).split()[0]
		Write.DATE = datetime.datetime( int("20"+Write.SPCdate.split("/")[2]), int(Write.SPCdate.split("/")[0]),int(Write.SPCdate.split("/")[1]) )
		Write.date = datetime.datetime.now()
		
		Write.obs = {'haz':None, 'sec':None, 'day':Write.date, 'ini':Write.init}
		Write.stack =[]

	
	def write_file(url, fyle):
		path = Write.REPO + Write.obs['ini'] +'Z' + Write.obs['day'].strftime('%d') + '/'
		
		if Write.obs['ini'] == '':
			path = Write.REPO + Write.init + 'Z' + Write.obs['day'].strftime('%d') + '/'

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
					   
			thermo	= [('SBCAPE','sbcp',True),
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
					   ('DCAPE','dcape'),
					   ('ETEMP','eltm')]
					   
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
					   ('3KmSHR','shr3'),
					   ('VTNMAG','vtm',True),
					   ('500mSRH','srh5'),
					   ('HODO','hodo')]
					   
			comp	= [('SCCOMP','scp'),
					   ('SIGTOR','stpc'),
					   ('1KmEHI','ehi1'),
					   ('3KmEHI','ehi3')]
					   
			frozen	= [('SFCTEMP','fztp'),
					   ('SFCBULB','swbt'),
					   ('MAXBULB','mxwb')]
					  
			severe	= thermo + shear + comp
			winter	= frozen
			
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
			current = True if Write.obs['ini'] == '' else False
			#archive = True if (Write.DATE - Write.obs['day']).total_seconds() > 432000 else False
			past = Write.obs['day'].strftime('%y%m%d')
			formdate = Write.obs['day'].strftime('%Y%m%d')
			parameter = petig	# assign petigre data as default params
			
			if not Write.obs['ini']=='':
				Write.obs['ini'] = Write.obs['ini'].zfill(2)		# zero fill init

			# build parameter list
			for item in Write.obs['haz']:
				# issues concating tuple list and dictionary tuple
				if item=='1' or item=='2':
					parameter += hazard[item]
				else:
					parameter.append( hazard[item] )
				
			# grab data!
			for s in Write.obs['sec']:
				for i in range(len(parameter)):
					if Write.archive:
						url = 'http://www.spc.noaa.gov/exper/ma_archive/images_s4/{date}/{init}_{param}'.format(date=formdate, init=Write.obs['ini'], param=parameter[i][1])
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
								url += 'sfc_' + past + '_' + Write.obs['ini'] + '00'
							elif parameter[i][0] == 'BR':
								url += 'rad_' + formdate + '_' + Write.obs['ini'] + '00'
							elif parameter[i][0] == 'VISSAT':
								url += 'vis_' + formdate + '_' + Write.obs['ini'] + '00'
							else:
								url += parameter[i][1] + '_' + past + Write.obs['ini']

					url += '.gif'
					
					fyle = parameter[i][0] + '~{init}Z-'.format(init=Write.init if Write.obs['ini'] ==  '' else Write.obs['ini']) + s[0] + '-' + formdate + '.gif'
					Write.write_file(url, fyle)
			
		# --------- end get_obs() ---------- #