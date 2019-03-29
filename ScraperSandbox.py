import os
import sys

import urllib.request
from bs4 import BeautifulSoup
import requests
import datetime
from datetime import date, timedelta
import time


class TestBed:

	REPO = 'C:\\Storm_Images\\NEW---TEMP\\TestBed\\'
	
	url = None
	date = None
	type = None
	
	def __init__(self):
		TestBed.url = "https://weather.msfc.nasa.gov/goes/abi/dynamic/GOES18172019088RHiLje.jpg"
		TestBed.type = "HISAT"
		
		TestBed.date = datetime.datetime.now()
	




	def write_file(url, fyle):
		path = TestBed.REPO + TestBed.type + "/"

		if not os.path.exists(path):
			os.makedirs(path)
		
		path = path + fyle
		with open(path, 'wb') as f:
				f.write( requests.get(url).content )		
		print(fyle)
		
		
		
	def ext_duration(beg, dur):
		begt = datetime.datetime(TestBed.date.year, TestBed.date.month, TestBed.date.day, beg, 0, 0)
		endt = begt + timedelta(hours =+ dur)
		curt = datetime.datetime.now()
		
		while (curt < endt):
			if ( (curt.minute%5) == 0 ):
				fyle = "VISSAT~" + curt.hour + curt.minute + ".gif"
				TestBed.write_file(TestBed.url, fyle)
			
			curt = datetime.datetime.now()
			
def main():

	start = None
	duration = None
	
	TestBed()
	
	os.system("cls")
	print( "Web Scraper Sandbox" )
	print( "for now...update URL in __init(...)__" )
	print( "Enter start hour (24hr CDT)")
	start = input( ">> " )
	print( "Enter duration in hours" )
	duration = input( ">> " )
	
	os.system("cls")
	print( "Running..." )
	print( "for next " + duration + " hours" )
	
	TestBed.ext_duration( int(start), int(duration) )
	
	print( "Scraping Complete\n" )
	input( "Press Enter" )
	
main()
	