#!/usr/bin/env python
import socket, ssl
import requests  # will make post requests to api
import json as j
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
ircsock.connect((server, 6697))  # Connect to the server using the port 6667
ircsock = ssl.wrap_socket(ircsock)
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

    sendmsg(channel, "Hey, bdbot is not done being build yet!!")

    if command == "help":
	sendmsg(channel, "umm, bdbot is, like, not even started yet :/ be back soon!")


# --- End bdbot's functions --- #


# --- Start Zuulbot's functions --- #


def zuulbot (usern, channel, command, arglist):
    weblocation = "http://zuul.cat.pdx.edu"
    print "zuulbot was called"

    if command == "help":
        sendmsg(channel, "(buy|purchase) $item: purchases an item")
        sendmsg(channel, "(finduser|fus) $user: display users bank")
        sendmsg(channel, "(finditem|fit) $item: display item price")
        sendmsg(channel, "(listitems|li): list's all items")
	sendmsg(channel, "you may /query b3nzerbot and use zuulbot: commands like normal")
	sendmsg(channel, "I also respond to zb or zb:")

    if command == "buy" or command == "purchase":
        sendmsg(channel, "still an alpha feature!!!!")
	purchase_item = ""
	for word in arglist:
	    if word != " ":
	        purchase_item += word + " " 
	purchase_item = purchase_item[:-1]
	print purchase_item

	#a bunch of special cases
	soda_list = ("coke", "pepsi", "sprite", "drpepper", "dr.pepper", "can", "soda", "mtdew", "mt.dew" "mountain dew")
	if purchase_item in soda_list:
	    purchase_item = "Canned Beverage"
		
        payload = {"name": usern, "item": purchase_item}
        r = requests.post(weblocation + "/newzuul/v1/purchase/", data=payload)
        if r.status_code == 200:
	    return_text = j.loads(r.text)
	    #sendmsg(channel, str(return_text))  # debugging lines
            #sendmsg(channel, str(r.text))  # debugging lines
	    if return_text["success"] == "false":
		sendmsg(channel, "benzer, halp! r.text['success'] is false!")
	    elif return_text["success"] == "true":
            	sendmsg(channel, "woot, worked")
            	sendmsg(channel, str(r.text))
	    else:
		sendmsg(channel, "benzer, halp! r.text['success'} != (true|false)")
        else:
            sendmsg(channel, "benzer, halp! r.status_code is %s" % str(r.status_code))

    if command == "finduser" or command == "fus":
	print "finduser was called"
	payload = {"name": arglist[0]}
	r = requests.post(weblocation + "/newzuul/v1/finduser/", data=payload)
	if r.status_code == 200:
            return_dict = j.loads(r.text)
	    if return_dict["success"] == "false":
		sendmsg(channel, "did not find: pleae check spelling")
	    elif return_dict["success"] == "true":
            	sendmsg(channel, "User: %s Has bank of: %s" % (str(return_dict["name"]), str(return_dict["bank"])))
	else:
	    sendmsg(channel, "benzer halp!!! r.status_code returned %" % str(r.status_code))

    if command == "finditem" or command == "fit":
	print "finditem was called"
	payload = {"name": arglist[0]}
	r = requests.post(weblocation + "/newzuul/v1/finditem/", data=payload)
	if r.status_code == 200:
            return_dict = j.loads(r.text)
	    if return_dict["success"] == "false":
		sendmsg(channel, "did not find: pleae check spelling")
	    elif return_dict["success"] == "true":
            	sendmsg(channel, "item: %s Costs: %s" % (str(return_dict["name"]), str(return_dict["cost"])))
	else:
	    sendmsg(channel, "benzer halp!!! r.status_code returned %" % str(r.status_code))

    if command == "listitems" or command == "li":
        print "listitems was called"
        payload = {"name": arglist[0], "item": arglist[1]}
        r = requests.post(weblocation + "/newzuul/v1/listall/", data=payload)
        if r.status_code == 200:
	    return_dict = j.loads(r.text)
            for item in return_dict:
                if item == "success":
                    continue
                else:
                    sendmsg(channel, "%s: %s" % (str(item), str	(return_dict[item])))
        else: sendmsg(channel, "benzer, halp! r.status_code was %s" % str(r.status_code))

# --- End Zuulbot's functions --- #

# --- Start Benzerbot's functions --- #


def benzerbot(user, channel, command, arglist):
    print "benzerbot was called"

    if command == "hello" or command == "hi" or command == "hola" or command == "oi" or command == "hey":
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

    if command == "help" or command == "halp" or command == "derp" or command == "wat" or command == "what":
        print "help was called"
        sendmsg(channel, "Commands:")
        sendmsg(channel, "(hello|hi|hey|oi|hola)")
        sendmsg(channel, "join $channel")
        sendmsg(channel, "join $channel permanently")
        sendmsg(channel, "you can also address:")
        sendmsg(channel, "zuulbot: help")
        sendmsg(channel, "bdbot: help")

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
        print "u: " + user
        print "c: " + channel
        print "b: " + addressing_bot
        print "c: " + command
        print "a: " + str(arglist)
        # - End debugging stuff - #

        if addressing_bot == "benzerbot" or addressing_bot == "bb":
            benzerbot(user, channel, command, arglist)

        if addressing_bot == "zuulbot" or addressing_bot == "zb":
            zuulbot(user, channel, command, arglist)

        if addressing_bot == "bdbot" or addressing_bot == "bd":
            bdbot(user, channel, command, arglist)

# --- End infinite loop to do bot things --- #

