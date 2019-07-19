import os
import sys

import urllib.request
from bs4 import BeautifulSoup
import requests
import datetime
from datetime import date, timedelta
import time


class Sonde:
	REPO = 'C:\\Storm_Images\\NEW---TEMP\\DataGrab\\'

	date = None
	init = None
	site = None


	def __init__(self):
		Sonde.date = None
		Sonde.init = []
		Sonde.site = []
		
		
	def write_file(url, fyle):
		path = Sonde.REPO +  'Soundings/'

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
		print( '#                    #' )
		print( '# RadioSonde Scraper #' )
		print( '#                    #' )
		print( '######################' )
		print()
		

	def site_menu():
		Sonde.header()
		
		print( 'Enter NWS RadioSonde site(s)' )
		print( '(separate sites with space)' )
		
		Sonde.site = input('\n>> ').upper().split()
		
		return Sonde.init_menu()
		
		
	def init_menu():
		Sonde.header()
		
		print( 'Enter initial time(s)' )
		print( '(separate initial times with a space' )
		
		Sonde.init = input('\n>> ')
		
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
		Sonde.site_menu()
		
		print( 'Sounding grab complete' )
		print( 'Quit (y/n)?' )
		
		
		
	


main()