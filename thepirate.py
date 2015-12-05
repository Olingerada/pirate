#!/usr/bin/env python


"""
The Pirate Bay scraper - This is the client

Uses 3 external libraries for scraping HTML elements from ThePirateBay and interacting with transmission-daemon.
Asks user for a search selection, offers a list of choices, and grabs the magnet link for the selection in a menu style fashion.

"""

__author__ = 'LANCE - https://github.com/lalanza808'


##################################################
# Libraries

# Built-in libraries
from os import path
import argparse

# 3rd party libraries
import requests
import bs4
import transmissionrpc

##################################################
# Variables

# Dictionaries/Arrays for storing search results
results = {}
links = []
choice = ""

# Current/working PirateBay URL
tpb = "https://thepiratebay.se"

# Torrent server IP; can be any machine running transmission-daemon 
# with a firewall inbound allowed to TCP/9091 (transmissionrpc)
rpcserver = 'localhost'

# Squelch HTTPS insecure warnings
requests.packages.urllib3.disable_warnings()

##################################################
# Parsing and Arguments

parser = argparse.ArgumentParser(description='Scrape The Pirate Bay for torrents.')

parser.add_argument('--search', '-s', dest='searcharg', help='The string to search for on TPB', required=False)

parser.add_argument('--top', '-t', dest='top', action='store_true', help='Automatically grab the torrent with most seeds', required=False)

parser.add_argument('--file', '-l', dest='file', help='Direct link to magnet or torrent file', required=False)

parser.add_argument('--url', '-u', dest='url', help='HTML page of the torrent file', required=False)

args = parser.parse_args()


##################################################
# Functions

def checkTransmission():
	"""
	Checks to see if transmission-daemon is running on rpcserver
	and and initiates the function to ask user for input
	"""
	try:
		transmissionrpc.Client(rpcserver, port=9091)
		getSearchURL()
	except KeyboardInterrupt:
		print "\n\nLater bro."
		exit(1)
	except transmissionrpc.error.TransmissionError:
		print "[!] Transmission-daemon not running on {}!".format(rpcserver)
		exit(2)

	
def getSearchURL():
	"""
	Takes input string to search for on TPB.
	Formats string into proper url
	Gets HTML source of search page for use in the next function
	"""
	if args.file:
		transmissionrpc.Client(rpcserver).add_torrent(args.file)
		exit(0)
	elif args.url:
		downloadTorrent(args.url)
		exit(0)
	elif args.searcharg:
		searchString = args.searcharg
	else:
		searchString = raw_input("[+] What would you like to search?\n>>> ")

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
	global links, results

	#Update the links array with the returned torrents
	pageSoup = bs4.BeautifulSoup(source) #Create Beautiful Soup object
	for link in pageSoup.find_all('a'): #Find all anchor elements in page source
		if link.get('href').startswith('/torrent'): #Filter items that don't start with /torrent
			links.append(link.get('href')) #Set the initial results to array 'links'
	

	#If -t is supplied, bypass this section of code and go on to download the top torrent
	if args.top and links:
		downloadTorrent("{}/{}".format(tpb, links[0]))
	else:
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
			args.searcharg = ''
			getSearchURL() #Loop back to script start

	
def chooseTorrent():
	"""
	Asks for selection of torrent, and prepares for the download
	"""
	global links, results

	try:
		selection = int(raw_input("\n[+] Enter the digit of the torrent to download.\n>>> "))
		if selection == 98:
			print "\nStarting over"
			results = {}
			links = []
			args.searcharg = ''
			getSearchURL() #Loop back to start
		elif selection == 99:
			print "\nBye.\n"
			exit() #Quit script
		elif selection in results: #If selection exists, set value to 'choice' variable
			choice = results[selection] #Updates variable based on key provided above, matches it with results dict
			downloadTorrent("{}/{}".format(tpb, choice))
		else: #If anything other than 98, 99, or valid key number entered, loop back to selection input
			print "\nNot a valid number"
			chooseTorrent()

	except ValueError:
		print "\nThat is not a digit."
		chooseTorrent()
	

def downloadTorrent(torrentURL):
	"""
	Grabs the first magnet link and initiates the download using the transmissionrpc python library
	"""
	
	magnetLinks = []
	
	torrentPage = requests.get(torrentURL, verify=False)
	torrentPageSoup = bs4.BeautifulSoup(torrentPage.content)
	
	for link in torrentPageSoup.find_all('a'):
		if str(link.get('href')).startswith('magnet:?xt'):
			magnetLinks.append(link.get('href'))
	
	magnetLink = magnetLinks[0]
	
	print "\n[+] Adding magnet link for torrent:\n\n{}".format(torrentURL)
	
	transmissionrpc.Client(rpcserver).add_torrent(magnetLink)

	print "\n[.] Done!\n"

	exit(0)	
	
if __name__ == "__main__":
	checkTransmission()
