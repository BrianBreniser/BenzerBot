#!/usr/bin/env python
import socket
#import time
# Some basic variables used to configure the bot
server = "irc.cat.pdx.edu"  # Server
channel = "#benzertest"  # Channel
botnick = "benzerbot"  # Your bots nick

# --- Start support functions --- #


def pong():
    ircsock.send("PONG :pingis\n")


def sendmsg(chan, msg):  # send msg to chan
    ircsock.send("PRIVMSG " + chan + " :" + msg + "\n")


def joinchan(chan):  # This function is used to join channels.
    ircsock.send("JOIN " + chan + "\n")

# --- End support functions --- #


# --- Start connect to shit -- #
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667))  # Connect to the server using the port 6667
ircsock.send("USER " + botnick + " " + botnick + " " + botnick +
    " :This is benzers bot\n")  # user authentication
ircsock.send("NICK " + botnick + "\n")  # Actually assign the nick to the bot


joinchan(channel)  # Join the channel using the functions we previously defined

# --- End connect to shit --- #


# -- Start infinite loop to do bot things --- #
while 1:  # Be careful with these! it might send you to an infinite loop
    ircmsg = ircsock.recv(2048)  # receive data from the server
    ircmsg = ircmsg.strip('\n\r')  # removing any unnecessary linebreaks.
    print ircmsg  # Here we print what's coming from the server

    if ircmsg.find("PING :") != -1:  # PONG on server PING
        pong()

    if ircmsg.find(":" + botnick + ": punch") != -1:
        ircsock.send("PRIVMSG " + channel + " :No. He's a nice guy!\n")

    if ircmsg.find(":" + botnick + ": hello") != -1:
        ircsock.send("PRIVMSG " + channel + " :hola\n")

# -- End infinite loop to do bot things --- #
