#!/usr/bin/env python

"""
This Python script combs through transmission downloads
and removes torrents at 100% fully downloaded. Great for keeping my
ISP off my back. Also sends a Pushbullet notification to my devices

Learn more about PushBullet here:
pushbullet.com
"""

__author__ = 'lance - github.com/lalanza808'


import transmissionrpc
import pushbullet
import requests
from time import sleep
from os import path

# Put your API key into a text file
apifile = path.expanduser('~/pb_api.txt')

# Get rid of the SSL warnings
requests.packages.urllib3.disable_warnings()

# Grab Pushbullet API
with open(apifile, 'rb') as file:
	api = file.read().strip()

##################################################
# Connect to services

t = transmissionrpc.Client('localhost', port=9091)
pb = pushbullet.Pushbullet(api)

for torrent in t.get_torrents():
	if torrent.percentDone == 1:
		print "[+] Removing torrent:\t{}".format(torrent.name)
		pb.push_note("Torrent Complete", torrent.name)
		sleep(3)
		t.remove_torrent(torrent.id)	
