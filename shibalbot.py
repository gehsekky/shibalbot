'''
ShibalBot

Created on Sep 14, 2011

taken from example at:
http://www.eflorenzano.com/blog/post/writing-markov-chain-irc-bot-twisted-and-python/

@author: andy
'''

import random
from twisted.internet import reactor
from twisted.words.protocols import irc
from twisted.internet import protocol

def is_valid_int(num):
    """Check if input is valid integer"""
    try:
        int(num)
        return True
    except ValueError:
        return False
        
class ShibalBot(irc.IRCClient):
    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)

    def signedOn(self):
        self.join(self.factory.channel)
        print "Signed on as %s." % (self.nickname,)

    def joined(self, channel):
        print "Joined %s." % (channel,)
        
    def privmsg(self, user, channel, msg):
        if self.factory.quotes_enabled:
            # handle quote command
            quotecommandprefix = "!"
            quotecommandtext = "quote"
            quotecommand = quotecommandprefix + quotecommandtext
            filename = "quotes.txt"
            if msg.startswith(quotecommand):
                # get action
                if msg == quotecommand:
                    # list random quote
                    with open(filename, "r") as quotefile:
                        lines = quotefile.readlines()
                        if not lines:
                            #empty file
                            msg = "empty file."
                            self.msg(channel, msg)
                            print msg
                        else:
                            # print random line
                            rand = random.randint(0, len(lines) - 1)
                            msg = "[" + str(rand) + "] " + lines[rand]
                            self.msg(channel, msg)
                            print msg
                else:
                    # get quote action
                    command_parts = msg.split(" ", 2)
                    if len(command_parts) < 3:
                        msg = "invalid number of command arguments"
                        self.msg(channel, msg)
                        print msg
                        # error
                    else:
                        # get command
                        if command_parts[1] == "add":
                            # check if there is a valid quote
                            line_to_add = command_parts[2]
                            if not line_to_add.endswith("\n"):
                                line_to_add = line_to_add + "\n"
                            with open(filename, "a") as quotefile:
                                quotefile.write(line_to_add)
                            msg = "quote added."
                            self.msg(channel, msg)
                            print msg
                        elif command_parts[1] == "delete":
                            # check if argument is valid int
                            if is_valid_int(command_parts[2]):
                                line_num = int(command_parts[2])
                            else:
                                msg = "command argument must be valid integer"
                                self.msg(channel, msg)
                                print msg
                                
                            if line_num > -1:
                                lines = None
                                with open(filename, "r") as quotefile:
                                    lines = quotefile.readlines()
                                if line_num < len(lines):
                                    lines.pop(line_num)
                                    with open(filename, "w") as quotefile:
                                        for line in lines:
                                            quotefile.write(line)
                                    msg = "deleted line #%s." % (line_num)
                                    self.msg(channel, msg)
                                    print msg
                                else:
                                    msg = "command argument exceeds number of lines in file"
                                    self.msg(channel, msg)
                                    print msg
                            else:
                                msg = "command argument must be non-negative"
                                self.msg(channel, msg)
                                print msg
                        elif command_parts[1] == "show":
                            # check if argument is valid int
                            if is_valid_int(command_parts[2]):
                                line_num = int(command_parts[2])
                            else:
                                msg = "command argument must be valid integer"
                                self.msg(channel, msg)
                                print msg
                                
                            if line_num > -1:
                                lines = None
                                with open(filename, "r") as quotefile:
                                    lines = quotefile.readlines()
                                if line_num < len(lines):
                                    msg = "[" + str(line_num) + "] " + lines[line_num]
                                    self.msg(channel, msg)
                                    print msg
                                else:
                                    msg = "command argument exceeds number of lines in file"
                                    self.msg(channel, msg)
                                    print msg
                            else:
                                msg = "command argument must be non-negative"
                                self.msg(channel, msg)
                                print msg
                        elif command_parts[1] == "search":
                                lines = None
                                with open(filename, "r") as quotefile:
                                    lines = quotefile.readlines()
                                results = ["[" + str(lines.index(line)) + "] " + line for line in lines if command_parts[2] in line > -1]
                                if len(results) > 0:
                                    for result in results[:3]:
                                        msg = result
                                        self.msg(channel, msg)
                                        print msg
                                else:
                                    msg = "no matches found for search phrase: %s" % (command_parts[2])
                                    self.msg(channel, msg)
                                    print msg
                        else:
                            #error
                            msg = "invalid command argument."
                            self.msg(channel, msg)
                            print(msg)
                        

class ShibalBotFactory(protocol.ClientFactory):
    protocol = ShibalBot

    def __init__(self, channel, nickname="ShibalBot", quotes=False, linkannouncer=False):
        self.channel = channel
        self.nickname = nickname
        self.quotes_enabled = quotes
        self.linkfetcher_enabled = linkannouncer

    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting." % (reason,)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)

if __name__ == "__main__":
    reactor.connectTCP("YOUR_IRC_SERVER_HOST", IRC_SERVER_HOST_PORT, ShibalBotFactory("YOUR_IRC_CHANNEL", "YOUR_IRCBOT_NICK", True, False))
    reactor.run()
