#!/usr/bin/env python
import socket
import requests  # will make post requests to api
#import time
# Some basic variables used to configure the bot
server = "irc.cat.pdx.edu"  # Server
botnick = "benzerbot"  # Your bots nick

# --- Start support functions --- #


def pong():
    ircsock.send("PONG :pingis\n")
    print "I PONG'd"


def sendmsg(chan, msg):  # send msg to chan
    ircsock.send("PRIVMSG " + chan + " :" + msg + "\n")


def joinchan(chan):  # This function is used to join channels.
    ircsock.send("JOIN " + chan + "\n")


def addchan(chan):
    channelz = open("channel_list", "a")
    channelz.write(chan + "\n")
    channelz.close()


def isadmin(usertocheck): #returns a string, not an int (why I have no fucking idea)
    myadmin = '0'
    admins = open("admins", "r")
    for admin in admins:
        admin = admin[:-1] #remove the newline from the file
        admin.lower()
        if admin == usertocheck.lower():
            myadmin = '1'
    admins.close()
    if myadmin == '1':
        print "an admin called this function"
    if myadmin == '0':
        print "not an admin called this function!!!"
    return myadmin


def addadmin(username):
    adminz = open("admins", "a")
    adminz.write(username.lower() + "\n")
    adminz.close()

# --- End support functions --- #


# --- Start connect to shit -- #
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667))  # Connect to the server using the port 6667
ircsock.send("USER " + botnick + " " + botnick + " " + botnick +
    " :This is benzers bot\n")  # user authentication
ircsock.send("NICK " + botnick + "\n")  # Actually assign the nick to the bot

#Open all channels in chanel_list file
channels = open("channel_list", "r")
for channel in channels:
    joinchan(channel)
channels.close()

# --- End connect to shit --- #

# --- Start bdbot's functions --- #


def bdbot(user, channel, command, arglist):
    print "bdbot was called"

    sendmsg(channel, "Hey, bdbot not done being build yet!!")


# --- End bdbot's functions --- #


# --- Start Zuulbot's functions --- #


def zuulbot (usern, channel, command, arglist):
    weblocation = "http://url/"
    print "zuulbot was called"

    if command == "help":
        sendmsg(channel, "(buy|purchase) $user $item: purchases an item")
        sendmsg(channel, "(finduser|fus) $user: display users bank")
        sendmsg(channel, "(finditem|fit) $item: display item price")
        sendmsg(channel, "(listitem|li): list's all items")

    if command == "buy" or command == "purchase":
        sendmsg(channel, "still an alpha feature!!!!")
        payload = {"name": arglist[0], "item": arglist[1]}
        r = requests.post(weblocation + "newzuul/v1/purchase/", data=payload)
        if r.status_code == 200:
            sendmsg(channel, "woot, worked")
            sendmsg(channel, str(r.text))
        else:
            sendmsg(channel, "benzer, halp! r.status did not respond 200")

    if command == "finduser" or command == "fus":
        sendmsg(channel, "this doesn't work yet :/")

    if command == "finditem" or command == "fit":
        sendmsg(channel, "this doesn't work yet :/")

    if command == "finduser" or command == "fus":
        sendmsg(channel, "this doesn't work yet :/")

# --- End Zuulbot's functions --- #

# --- Start Benzerbot's functions --- #


def benzerbot(user, channel, command, arglist):
    print "benzerbot was called"

    if command == "hello":
        print "hello was called"
        sendmsg(channel, "hola %s" % user)

    if command == "join":
        print "join was called"
        anadmin = isadmin(user)
        if anadmin == '1':
            sendmsg(channel, "Okay, i'll join %s, %s" % (arglist[0], user))
            joinchan(arglist[0])

            if arglist[1].lower() == "permanently":
                print "permanent join list was called"
                sendmsg(channel, "i'll even join %s permanently!" % arglist[0])
                addchan(arglist[0])

        elif anadmin == '0':
            sendmsg(channel, "But, I don't take orders from %s" % user)
        else:
            sendmsg(channel, "Benzer, help, I got %s" % isadmin)

    if command == "addadmin":
        print "newadmin was called"
        anadmin = isadmin(user)
        if anadmin == '1':
            sendmsg(channel, "okay, %s is now an admin" % arglist[0])
            addadmin(arglist[0])
        elif anadmin == '0':
            sendmsg(channel, "But, I don't take orders from %s" % user)
        else:
            sendmsg(channel, "benzer, help, I got %s" % isadmin)

    if command == "help":
        print "help was called"
        sendmsg(channel, "Hi, this is the benzerbot help command! Lets go over some basics:")
        sendmsg(channel, "")
        sendmsg(channel, "")
        sendmsg(channel, "")
        sendmsg(channel, "")
        sendmsg(channel, "")
        sendmsg(channel, "")
        sendmsg(channel, "")

    if command == "pme":
        print "pme was called"
        sendmsg(user, "you told me to PM you: %s" % arglist[0])

# --- End Benzerbot's functions --- #

# --- Start infinite loop to do bot things --- #
while 1:  # Be careful with these! it might send you to an infinite loop
    ircmsg = ircsock.recv(2048)  # receive data from the server
    ircmsg = ircmsg.strip('\n\r')  # removing any unnecessary linebreaks.
    print ircmsg  # Here we print what's coming from the server

    #imediatly PONG
    if ircmsg.find("PING") != -1:  # PONG on server PING
        pong()

    #Kicks if somebody talks
    if ircmsg.find("PRIVMSG"):
        splitircmsg = ircmsg.split() + [" ", " ", " "]  # cuts string
        user = str(splitircmsg[0].split("!")[0]).replace(":", "")  # user
        channel = str(splitircmsg[2]).lower()  # the channel

        if channel == "benzerbot" or channel == "zuulbot" or channel == "bdbot":  # if channel is pm window
            channel = user  # makes PM's work

        addressing_bot = str(splitircmsg[3]).replace(":", "").lower()  # the bot the command will be sent too
        command = str(splitircmsg[4]).lower()  # the command sent to the bot
        command = command.lower()  # i'd rather not screw with caps problems
        arglist = splitircmsg[5:]  # arglist for the command

        # - Debugging stuff, uncomment to see 'log' - #
        #print user
        #print channel
        #print addressing_bot
        #print command
        #print arglist
        # - End debugging stuff - #

        if addressing_bot == "benzerbot":
            benzerbot(user, channel, command, arglist)

        if addressing_bot == "zuulbot":
            zuulbot(user, channel, command, arglist)

        if addressing_bot == "bdbot":
            bdbot(user, channel, command, arglist)

# --- End infinite loop to do bot things --- #

