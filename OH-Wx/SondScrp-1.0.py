import os
import sys

import urllib.request
import requests


class Sonde:
	REPO = 'W:\\WxEvents\\NEW---TEMP\\'

	date = None
	init = None
	site = None


	def __init__(self):
		Sonde.date = ''
		Sonde.init = []
		Sonde.site = []
		
		
	def write_file(url, fyle):
		path = Sonde.REPO +	 'Soundings/'

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
		
	
	def get_sond():
		url = ''
		fyle = ''
		
		for i in Sonde.init:
			for s in Sonde.site:
				url = "https://www.spc.noaa.gov/exper/soundings/"
				url += Sonde.date + i + "_OBS/" + s + ".gif"
				fyle = "SKEW-T&HODO~" + i + "Z-K" + s + "-20" + Sonde.date + ".gif"
				
				Sonde.write_file(url,fyle)
				
	
	def header():
		os.system("cls")
		print( '######################' )
		print( '#					 #' )
		print( '# RadioSonde Scraper #' )
		print( '#					 #' )
		print( '######################' )
		print()
		

	def indv_menu():
		Sonde.header()
		
		print( 'Enter NWS RadioSonde site(s)' )
		print( '(separate sites with space)' )
		
		Sonde.site = input('\n>> ').upper().split()
		
		return Sonde.init_menu()


	def regn_menu():
		regions = { 'NE':['APX','DTX','ILN','RNK','WAL','IAD','PIT','BUF','ALB','OKX','CHH','GYX','CAR'],
					'EC':['ILN','BNA','BMX','TLH','FFC','GSO','RNK','PIT','IAD','WAL','MHX','CHS','JAX'],
					'MW':['UNR','LBF','DDC','OUN','LZK','SGF','TOP','OAX','ABR','MPX','DVN','ILX','ILN','BNA','GRB','DTX'],
					'SP':['DNR','ABQ','EPZ','DRT','MAF','AMA','DDC','TOP','OUN','FWD','CRP','LCH','SHV','LZK','SGF'],
					'CP':['ABQ','DNR','RIW','UNR','LBF','DDC','OUN','AMA','TOP','OAX','ABR','MPX','GRB','DVN','ILX','SGF','LZK'],
					'NP':['DNR','RIW','TFX','GGW','UNR','LBF','OAX','DVN','GRB','MPX','INL','ABR','BIS'],
					'SE':['LCH','SHV','LZK','BNA','JAN','LIX','BMX','FFC','TLH','JAX','TBW','CHS','GSO','MHX','RNK','WAL'],
					'FL':['TLH','JAX','TBW','KEY','MFL'],
					'':True}
		
		Sonde.header()
		
		# !!! Expand to enter multiple Regions !!!
		
		print( 'Enter Region' )
		print()
		print( '##################' )
		print( '# NE - Northeast #' )
		print( '# EC - E. Coast	 #' )
		print( '# SP - S. Plains #' )
		print( '# CP - C. Plains #' )
		print( '# NP - N. Plains #' )
		print( '# MW - Midwest	 #' )
		print( '# SE - Southeast #' )
		print( '# FL - Florida	 #' )
		print( '##################' )
		
		Sonde.site = regions[ input('\n>> ').upper() ]
		
		if Sonde.site:
			return Sonde.indv_menu()
		else:
			return Sonde.init_menu()
		
	
	def init_menu():
		Sonde.header()
		
		print( 'Enter initial time(s)' )
		print( '(separate initial times with a space' )
		
		

		
		Sonde.init = input('\n>> ').split()
		
		return Sonde.date_menu()
	
	
	def date_menu():
		Sonde.header()
		
		print( 'Enter date (YYMMDD)' )
		
		Sonde.date = input('\n>> ')
		
		return Sonde.get_sond()
		
		
def main():
	quit = False
	Sonde()
	
	while( not quit ):
		Sonde.regn_menu()
		
		print( 'Sounding grab complete' )
		print( 'Quit (y/n)?' )
		
		
		
	


main()