import os
import sys

import urllib.request
from bs4 import BeautifulSoup
import requests
import datetime
from datetime import date, timedelta
import time


class TestBed:

	REPO = 'C:\\WxEvents\\NEW---TEMP\\TestBed\\'
	
	url = None
	date = None
	type = None
	
	def __init__(self):
		TestBed.url = "https://weather.msfc.nasa.gov/cgi-bin/get-abi?satellite=GOESEastconusband02&lat=35&lon=-97&zoom=1&width=1400&height=1000&quality=100"
		TestBed.type = "HISAT"
		
		TestBed.date = datetime.datetime.now()
	
	
	def write_file(url, fyle, dir):
		path = TestBed.REPO + dir	#+ TestBed.type + "/"

		if not os.path.exists(path):
			os.makedirs(path)
		
		path = path + fyle
		with open(path, 'wb') as f:
				f.write( requests.get(url).content )		
		print(fyle)
		
		print(url + "\n")
		
			
	def hires_goes(beg, dur):
		begt = datetime.datetime(TestBed.date.year, TestBed.date.month, TestBed.date.day, beg, 0, 0)
		endt = begt + timedelta(hours =+ dur)
		curt = datetime.datetime.now()
		
		page = None
		url = None
		
		while (curt < endt):
			if ( (curt.minute%5) == 0 ):
				page = urllib.request.urlopen(TestBed.url).read()
				images = BeautifulSoup(page, 'html.parser').findAll('img')
				url = "https://weather.msfc.nasa.gov" + images[0]['src']

				fyle = "VISSAT~" + str(curt.hour) + str(curt.minute) + ".gif"	# could change minute to -8 for actual time, consider bounds min<8
				TestBed.write_file(url, fyle)
				
				time.sleep(65)	# only scrape once
			
			curt = datetime.datetime.now()
	

	def get_sonde(sites, date, init):
		for site in sites:
			url = "https://www.spc.noaa.gov/exper/soundings/"
			url += date + init + "_OBS/" + site + ".gif"
			fyle = "SKEW-T&HODO~" + init + "Z-K" + site + "-20" + date + ".gif"
			TestBed.write_file(url, fyle)


	def min_goes(beg, end, sec):
		dir = "\\1mg\\"
        
        #sec = {
         #   "M1B2S1":"mesoscale_01_band_02_sector_01/mesoscale_01_band_02_sector_01_",
        #    "M1B2S5":"mesoscale_01_band_02_sector_05/mesoscale_01_band_02_sector_05_"
        #}
		
        
        # need to implement full date, not just beginning / ending hour
		begt = beg + timedelta(hours =+ 6)	# convert to UTC ;  MUST CHANGE W/ DST
		endt = end + timedelta(hours =+ 6)	# convert to UTC ;  MUST CHANGE W/ DST

		while begt < endt:
			url = "http://rammb.cira.colostate.edu/ramsdis/online/images/goes-16/mesoscale_01_band_02_sector_05/mesoscale_01_band_02_sector_05_" + \
			"{date}22.gif".format( date = begt.strftime("%Y%m%d%H%M") )
		
			fyle = "BD02~{hm}Z-GOES16-{ymd}.gif".format(hm=begt.strftime("%H%M"), ymd=begt.strftime("%y%m%d"))
			TestBed.write_file(url, fyle, dir)
			begt = begt + timedelta(minutes =+ 1)

	
	def get_1minG(beg, dur):
		dir = "\\1mg\\"
		'''
        sec = {("M1B2S1":"mesoscale_01_band_02_sector_01/mesoscale_01_band_02_sector_01_"),
               ("M1B2S5":"mesoscale_01_band_02_sector_05/mesoscale_01_band_02_sector_05_")}
		'''
        
        
		begt = datetime.datetime(TestBed.date.year, TestBed.date.month, TestBed.date.day, beg, 0,0)
		endt = begt + timedelta(hours =+ dur+5)									# convert to UTC
		curt = datetime.datetime.now() + timedelta(hours =+ 5, minutes =- 30)	# convert to UTC
		
		#url = "http://rammb.cira.colostate.edu/ramsdis/online/images/goes-16/mesoscale_01_band_02_sector_01/mesoscale_01_band_02_sector_01_"
		
		while (curt < endt):
			url = "http://rammb.cira.colostate.edu/ramsdis/online/images/goes-16/mesoscale_01_band_02_sector_01/mesoscale_01_band_02_sector_01_" + \
			      "{date}23.gif".format( date = curt.strftime("%Y%m%d%H%M") )
			fyle = "BD02~{hm}Z-GOES16-{ymd}.gif".format(hm=curt.strftime("%H%M"), ymd=curt.strftime("%Y%m%d"))
			TestBed.write_file(url, fyle, dir)
			time.sleep(60)	# only pull data once per minute
			curt = datetime.datetime.now() + timedelta(hours =+ 5, minutes =- 30)	# convert to UTC
	
	
def main():

	start = None
	duration = None
	
	TestBed()
	
	os.system("cls")
	print( "Web Scraper Sandbox" )
	print( "-------------------" )
# ----------------------------------- #
# ---- N E W   C O D E   H E R E  --- #

	print( "Enter start time in CD/ST (24hr):" )
	beg = int( input("\n>> ") )
	print( "Enter duration in hours:" )
	dur  = int( input("\n>> ") )
	
	TestBed.min_goes(beg, dur, "M1B2S5")
	
	
	
	'''
	begt = datetime.datetime(TestBed.date.year, TestBed.date.month, TestBed.date.day, beg, 0, 0)
	endt = datetime.datetime(TestBed.date.year, TestBed.date.month, TestBed.date.day, dur, 0, 0)
	TestBed.min_goes(begt, endt)
	
	
	print( "Enter Sounding Sites (SSS) separated by a space:")
	sites = input( ">> " )
	sites = sites.upper().split()
	print( "Enter init time:" )
	init = input( ">> ")
	print( "Enter date (yymmdd):" )
	date = input( ">> ")
	TestBed.get_sonde(sites, date, init)
	
	
	print( "for now...update URL in __init(...)__" )
	print( "Enter start hour (24hr CDT)")
	start = input( ">> " )
	print( "Enter duration in hours" )
	duration = input( ">> " )
	
	os.system("cls")
	print( "Running..." )
	print( "for next " + duration + " hours" )
	
	TestBed.hires_goes( int(start), int(duration) )
	
	print( "Scraping Complete\n" )
	input( "Press Enter" )
	'''
	
main()
	