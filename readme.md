# Pirate

Command line torrent downloader. 

Parses HTML pages on [ThePirateBay](https://thepiratebay.se) based on a search string provided. Downloads torrents using transmission-daemon.

Initially made for the older version with torrents hosted from a separate subdomain, but now modified for grabbing magnet links instead.

----

### Requirements

This script was written in Python version 2.7. Version 3 compatibility requires rewriting some code, and may be done at a later time. Pull requests welcome.

This script depends on 3 external Python libraries. Please ensure the following are installed to the system:

 * transmissionrpc
 * requests
 * beautifulsoup4

If pip is installed, just run the following as root:

```
pip install transmissionrpc requests beautifulsoup4
```

### Usage

Place the script somewhere in your executable path. I like ~/bin

```
$ mkdir ~/bin
$ echo 'PATH=$PATH:~/bin' >> ~/.bashrc && source ~/.bashrc
$ cp pirate/pirate.py ~/bin
```

Then just run it

```
$ pirate.py
```

The rest is self explanatory

**BONUS**
Add a cron job to run //removeFinishedTorrents.py// every 5 minutes. Hook it into [PushBullet](https://pushbullet.com) for mobile notifications.

#### TODO

 * Refactor code; not a fan of the spaghetti code functions
 * Comment script better; for personal reasons. I hate being confused 6 months later
 * Maybe add a setup script. Maybe
