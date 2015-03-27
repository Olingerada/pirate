#!/usr/bin/env python


"""
The Pirate Bay scraper -

Uses 2 external libraries for scraping HTML elements from ThePirateBay.
Asks user for a search selection, offers a list of choices, and grabs the magent link for the selection.

"""

__author__ = 'LANCE'


# Built-in libraries
import urllib3
from platform import system as operatingSystem
from os import path, system
from urllib import urlretrieve
from re import search
from time import sleep

# 3rd party libraries
import requests
import bs4


results = {}
links = []
choice = ""
tpb = "https://thepiratebay.se"

# Squelch SSL warnings
urllib3.disable_warnings()
	
def getSearchURL():
	"""
	Takes input string to search for on TPB.
	Formats string into proper url
	"""
	try:
		searchString = raw_input("[+] What would you like to search?\n>")
	except KeyboardInterrupt:
		print "\n\nLater bro."
		exit(0)
	searchURL = "{}/search/{}/0/7/0".format(tpb, searchString) #/0/7/0 tells TPB to sort descending by seeds
	pageSource = requests.get(searchURL, verify=False).text #Use requests lib to fetch page source for bs4 parsing
	analyzeURL(pageSource) #Run analyzeURL function, passing page source
	

def analyzeURL(source):
	"""
	Takes the page source and parses it with BeautifulSoup.
	Finds all anchor elements on the page, pre-sorted by seeders
	Enumerates list of elements, and adds them to results dictionary
	"""
	print "\n"
	global links
	global results

	pageSoup = bs4.BeautifulSoup(source) #Create Beautiful Soup object
	for link in pageSoup.find_all('a'): #Find all anchor elements in page source
		if link.get('href').startswith('/torrent'): #Filter items that don't start with /torrent
			links.append(link.get('href')) #Set the initial results to array 'links'

	for number,link in enumerate(links): #Enumerate the array so the numbers start at 0
		results.update({number:link}) #Append results to results dictionary
		print "({}) {}".format(number, path.basename(link))

	if results: #If dict is not empty, continue with script
		print "\n(98) Search again"
		print "(99) Exit"
		chooseTorrent()
	else: #If dict is empty (no results from search) re-run script
		print "\nNo results found. Try again."
		results = {}
		links = []
		getSearchURL() #Loop back to script start

	
def chooseTorrent():
	"""
	Asks for selection of torrent, and prepares for the download
	"""
	global links, results
	try:
		selection = int(raw_input("\n*** Enter the digit of the torrent to download.\n>"))
		if selection == 98:
			print "\nStarting over"
			results = {}
			links = []
			getSearchURL() #Loop back to start
		elif selection == 99:
			print "\nBye.\n"
			exit() #Quit script
		elif selection in results: #If selection exists, set value to 'choice' variable
			choice = results[selection] #Updates variable based on key provided above, matches it with results dict
			downloadTorrent(choice)
		else: #If anything other than 98, 99, or valid key number entered, loop back to selection input
			print "\nNot a valid number"
			chooseTorrent()
	except ValueError:
		print "\nThat is not a digit."
		chooseTorrent()
	

def downloadTorrent(torrent):
	"""
	Grabs the first magnet link and initiates the download
	"""
	# TPB no longer uses torrents as subdomain. Changing script to direct add magnet links
	#torrentName = search("/torrent/(.*)", torrent) #Strip out first portion of string (/torrent/)
	#torrentURL = "https://torrents.thepiratebay.se/{}.torrent".format(torrentName.group(1)) #TPB uses subdomain 'torrents' to host .torrent files

	magnetLinks = []
	torrentPage = requests.get("{}/{}".format(tpb, torrent), verify=False)
	torrentPageSoup = bs4.BeautifulSoup(torrentPage.content)
	for link in torrentPageSoup.find_all('a'):
		if str(link.get('href')).startswith('magnet:?xt'):
			magnetLinks.append(link.get('href'))
	torrentURL = magnetLinks[0]
	print "\n*** Adding magnet link:\n\n{}".format(torrentURL)
	#urlretrieve(torrentURL, path.basename(torrentURL)) #Save torrent file as same name
	checkOS(path.basename(torrentURL)) #Check host operating system for proper torrent client


def checkOS(torrentDownload):
	"""
	Checks host operating system and determines how to start the torrent transfer
	"""
	if operatingSystem() == "Windows": #Windows is finished at this point
		openCode = system("start {}".format(torrentDownload)) #Simply open it, default torrent client opens
		if openCode == 0:
			exit(0) #Clean exit
		else:
			print "\nYou need a torrent client installed.\n"
			exit(1)
	else:
		checkTransmission(torrentDownload) #For linux systems running transmission-cli
		
def checkTransmission(torrentDownload):
	"""
	Checks for the existence of transmission-remote, necessary for starting torrents
	"""
	whichCode = system("which transmission-remote")
	print "\n"
	if whichCode == 0:
		system("transmission-remote localhost:9091 -a {}".format(torrentDownload))
		
	
if __name__ == "__main__":
	getSearchURL()
