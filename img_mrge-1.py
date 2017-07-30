###############
# Image Merge #
###############


import os
import sys
import requests

from PIL import Image

REPO = 'C:/Users/anwalters/Scripts/'

def main():
	fg = Image.open(REPO + 'map.gif').convert('RGBA')
	#bg = Image.open(REPO + 'vis.gif').convert('RGBA')
	
	url = 'http://climate.cod.edu/data/satellite/2km/IL_IN/vis/IL_IN.vis.20170726.1130.gif'
	bg = Image.open( requests.get(url, stream=True).raw ).convert('RGBA')
	
	#bg.show()
	
	bg.paste(fg, None, fg)
	
	# save in PNG for lower data loss
	bg.save(REPO+"sat.png","PNG")
	

main()