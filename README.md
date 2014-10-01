shibalbot
=========

an extremely simple python irc bot.

I wrote this bot so I could learn more about python. So far it only 
parses incoming messages to the user and channel, prints out the title of a link if detected, and has a quote
module.

###requirements
* python 2.7
* twisted
* zope.interface
* BeautifulSoup

###getting started
Make a file in the same folder containing the shibalbot.py script called "shibalbot.config" and put the following inside it:

    [core]
    host: your.ircserver.org
    port: 6667
    channel: #bots
    botname: yourbotname
    
    [commands]
    prefix: !

###TODO
* make a plugin system (nothing complicated, just a way to add more functions without hardcoding a bunch of stuff)
