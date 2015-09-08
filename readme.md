# Pirate.py

Command line torrent downloader with [Pushbullet](https://pushbullet.com) notifications.	

Default behavior parses HTML pages on [ThePirateBay](https://thepiratebay.se) based on a search string provided, then passes the magnet link to a locally running Transmission-Daemon (localhost or same LAN). 

Can also add direct HTML pages of the desired torrent with --url, and direct magnet links and torrent files with --file.

----

### Requirements

#### Client Side (pirate.py)

This script was written in Python version 2.7. Version 3 compatibility requires rewriting some code, and may be done at a later time. Pull requests welcome.

3 external Python libraries needed. Please ensure the following are installed to the system:

 * transmissionrpc
 * requests
 * beautifulsoup4

If pip is installed, just run the following as root:

```
$ pip install transmissionrpc requests beautifulsoup4
```

Then edit the pirate.py file, and change the __rpcserver__ variable to the server's IP/hostname (if not localhost)


#### Server Side (transmission-daemon and pirate-remote.py)

Transmission-daemon needs to be installed for downloading torrents and TCP/9091 needs to be opened on the computer's firewall

RHEL/CentOS/Fedora (yum)

```
$ yum install transmission-daemon transmission-cli 
$ firewall-cmd --add-port=9091/tcp --permanent
```

Debian/Ubuntu (apt)

```
$ apt-get install transmission-daemon transmission-cli
$ iptables -A INPUT -p tcp --dport 9091 -j ACCEPT
```

[pushbullet.py](https://github.com/randomchars/pushbullet.py) is needed for Pushbullet notifications.

```
$ pip install pushbullet.py
```

Put your PushBullet API key in api variable in the script and set a cron job to run pirate-remote.py every X minutes.

Make sure the server running Transmission (if not localhost) is accepting traffic on TCP/9091 and RPC is enabled in the Transmission settings.json file. Read about configuring Transmission [here](https://trac.transmissionbt.com/wiki/EditConfigFiles).


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


#### TODO

 * Refactor code; not a fan of the spaghetti code functions
 * Comment script better; for personal reasons. I hate being confused 6 months later
 * Pushbullet read/download new torrents
