import os
import sys

import urllib.request
import requests


class Sonde:
	REPO = ''

	date = None
	init = None
	site = None 
	archive = None


	def __init__(self):
		Sonde.date = ''
		Sonde.init = []
		Sonde.site = []
		Sonde.archive = False
		
		
	def write_file(url, fyle):
		path = Sonde.REPO

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
				if Sonde.archive:
					# need url to keep Sonde.date for 00Z init on next day
					url = "https://www.spc.noaa.gov/exper/archive/events/20" + Sonde.date + "/soundings/"
					url += Sonde.date + i + "_SNDG/" + s + ".gif"
				else:
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
					'FL':['TLH','JAX','TBW','KEY','MFL']}
					#'':"gumbo"}
		
		Sonde.header()
		
		# !!! Expand to enter multiple Regions !!!
		
		print( 'Enter Region(s)' )
		print( '(separate Regions with a space' )
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
		
		
		temp = input('\n>> ')
		if temp == '':
			return Sonde.indv_menu()
		else:
			temp = temp.upper().split()
			for r in temp:
				Sonde.site += regions[r]
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
		
		print()
		print( 'Archive?' )
		print( '1. Yes' )
		Sonde.archive = True if input('\n>> ') == '1' else False
		
		return Sonde.get_sond()
		
		
		
def main():
	quit = False
	Sonde()
	
	os.system("cls")
	print( "Sounding Scraper" )
	print( "----------------" )
	print( "Enter path:" )
	Sonde.REPO = input( "\n>> " ) + '\\'
	
	while( not quit ):
		Sonde()
		Sonde.regn_menu()
		
		print( 'Sounding grab complete' )
		print( 'Quit (y/n)?' )
		quit = True if input('\n>> ') == 'y' else False
        
    os.system("cls")
		
		
		
	


main()