# Pirate

Command line HTML parser/scraper used for grabbing torrents from [ThePirateBay](https://thepiratebay.se). Downloads torrents using command line program, transmission-daemon.

Initially made for the older version with torrents hosted from a separate subdomain, but now modified for grabbing magnet links instead.

----

## Requirements

This script was written in Python version 2.7. Version 3 compatibility requires rewriting some code, and may be done at a later time. Pull requests welcome.

This script depends on 3 external Python libraries. Please ensure the following are installed to the system:

 * transmissionrpc
 * requests
 * beautifulsoup4

If pip is installed, just run:

```
pip install transmissionrpc requests beautifulsoup4
```

## Usage

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

## TODO

 * Refactor code; not a fan of the spaghetti code functions
 * Comment script better; for personal reasons. I hate being confused 6 months later
 * Maybe add a setup script. Maybe
