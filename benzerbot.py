#!/usr/bin/env python
""" A python bot with multiple functions. """
import socket
import ssl
import requests  # will make post requests to api
import json as j
from time import sleep, time
# import time
# Some basic variables used to configure the bot
server = "irc.cat.pdx.edu"  # Server
botnick = "bb"  # Your bots nick
password = "benzerbot"

timestamp = time()

# --- Start support functions --- #


def pong():
    """ Keep bot alive to server. """
    ircsock.send("PONG :pingis\n")
    print "I PONG'd"


def sendmsg(chan, msg):  # send msg to chan
    """ general sendmsg function. """
    global timestamp
    while time() <= timestamp + 1:
        sleep(.1)
    ircsock.send("PRIVMSG " + chan + " :" + msg + "\n")
    timestamp = time()


def joinchan(chan):  # This function is used to join channels.
    """ simple joinchan function. """
    ircsock.send("JOIN " + chan + "\n")


def addchan(chan):
    """ simple add channel function. """
    channelz = open("channel_list", "a")
    channelz.write(chan + "\n")
    channelz.close()


def isadmin(usertocheck):  # returns a string, not an int (why I have no fucking idea)
    """ Check to see if the user is admin."""
    myadmin = '0'
    admins = open("admins", "r")
    for admin in admins:
        admin = admin[:-1]  # remove the newline from the file
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
    """add an admin."""
    adminz = open("admins", "a")
    adminz.write(username.lower() + "\n")
    adminz.close()


def concat_list(list_in):  # Creates strings (with spaces) out of a list sent in
    """Concat a list of strings into one string."""
    print "concat_list was called"
    my_string = ""
    for word in list_in:
        if word != " ":
            my_string += word + " "
    my_string = my_string[:-1]
    return my_string

# --- End support functions --- #


# --- Start connect to shit -- #
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6697))  # Connect to the server using the port 6667
ircsock = ssl.wrap_socket(ircsock)
ircsock.send("USER " + botnick + " " + botnick + " " + botnick +
             " :This is benzers bot\n")  # user authentication
ircsock.send("NICK " + botnick + "\n")  # Actually assign the nick to the bot
ircsock.send("PRIVMSG NickServ :" + 'IDENTIFY ' + password + "\n")


# Open all channels in chanel_list file
channels = open("channel_list", "r")
for channel in channels:
    joinchan(channel)
channels.close()

# --- End connect to shit --- #

# --- Start bdbot's functions --- #


def bdbot(user, channel, command, arglist):
    """will never be built :(."""
    print "bdbot was called"

    sendmsg(channel, "Hey, bdbot is not done being build yet!!")

    if command == "help":
        sendmsg(channel, "umm, bdbot is, like, not even started yet :/ be back soon!")


# --- End bdbot's functions --- #


# --- Start Zuulbot's functions --- #

# - Helper Functions - #


def finduser(usern, channel, quiet=False):
    """Find a user."""
    print "finduser helper function was called"
    weblocation = "http://zuul.cat.pdx.edu"

    # One "special" persons case for one person who feels their username should not be their zuulname too ;)
    # if str(usern) == str("zaalatta"):
    #     usern = "zolo"

    payload = {"name": usern}
    r = requests.post(weblocation + "/newzuul/v1/finduser/", data=payload)
    if r.status_code == 200:
        return_dict = j.loads(r.text)
        if return_dict["success"] == "true":
            if quiet is False:
                sendmsg(channel, "User: %s Has bank of: %s" % (str(return_dict["name"]), str(return_dict["bank"])))
            return True, str(return_dict["name"]), str(return_dict["bank"])
    else:
        sendmsg(channel, "benzer, halp!!! r.status_code returned %" % str(r.status_code))
    return False, "none", "none"


def finditem(item_name, channel, quiet=False):
    """Find an item."""
    print "finditem helper function called"
    weblocation = "http://zuul.cat.pdx.edu"

    # a bunch of special purchase cases
    soda_list = ("coke", "pepsi", "sprite", "drpepper", "dr.pepper", "can",
                 "soda", "mtdew", "mt.dew", "mountain dew")

    if item_name.lower() in soda_list:
        item_name = "Canned Beverage"

    if item_name.lower() == "cheese":
        item_name = "String Cheese"

    if item_name.lower() == "rice krispies":
        item_name = "Rice Krispies Bar"

    if item_name.lower() == "granola":
        item_name = "Granola Bar"

    payload = {"name": item_name}
    r = requests.post(weblocation + "/newzuul/v1/finditem/", data=payload)
    if r.status_code == 200:
        return_dict = j.loads(r.text)
        if return_dict["success"] == "true":
            if quiet is False:
                sendmsg(channel, "item: %s Costs: %s" % (str(return_dict["name"]), str(return_dict["cost"])))
            return True, str(return_dict["name"]), str(return_dict["cost"])
    else:
        sendmsg(channel, "benzer, halp!!! r.status_code returned %" % str(r.status_code))
    return False, "none", "none"


def purchaseitem(usern, item_name, channel):
    """Purchase an item using the username that called the function."""
    print "purchaseitem helper function called"
    weblocation = "http://zuul.cat.pdx.edu"

    payload = {"name": usern, "item": item_name}
    r = requests.post(weblocation + "/newzuul/v1/purchase/", data=payload)
    if r.status_code == 200:
        return_text = j.loads(r.text)
        # sendmsg(channel, str(return_text))  # debugging lines
        # sendmsg(channel, str(r.text))  # debugging lines
        if return_text["success"] == "false":
            sendmsg(channel, "The Purchase was unsuccessful, is your username added to zuul? Is the item's name correct? ")
        elif return_text["success"] == "true":
            return True
    else:
        sendmsg(channel, "benzer, halp! r.status_code is %s" % str(r.status_code))


def addtobank(usern, ammount, channel):
    """add monies to bank for user."""
    print "addtobank helper function called"
    weblocation = "http://zuul.cat.pdx.edu"

    payload = {"name": usern, "ammount": ammount}
    r = requests.post(weblocation + "/newzuul/v1/addbank/", data=payload)
    if r.status_code == 200:
        return_text = j.loads(r.text)
        # sendmsg(channel, str(return_text))  # debugging lines
        # sendmsg(channel, str(r.text))  # debugging lines
        if return_text["success"] == "false":
            sendmsg(channel, "error code: " + str(return_text["error"]))
        elif return_text["success"] == "true":
            return True
    else:
        sendmsg(channel, "benzer, halp! r.status_code is %s" % str(r.status_code))
        return False


def addfunds(usern, ammount):
    """ add arbitrary funds to users bank. """
    print "addfunds wrapper function called"
    weblocation = "http://zuul.cat.pdx.edu"

    payload = {"name": usern, "ammount": ammount}
    r = requests.post(weblocation + "/newzuul/v1/???/", data=payload)
    r.status_code

# - End Helper Functions - #


def zuulbot(usern, channel, command, arglist):
    """number of commands for zuulbot."""
    weblocation = "http://zuul.cat.pdx.edu"
    print "zuulbot was called"

    # One "special" persons case for one person who feels their username should not be their zuulname too ;)
    if str(usern) == str("zaalatta"):
        usern = "zolo"

    if command == "help" or command == "halp" or command == "?" or command == "-help" or command == "--help":
        sendmsg(channel, "I respond to zuulbot, zuulbot:, zb or zb:")
        sendmsg(channel, "(buy|purchase) $item: purchases an item")
        sendmsg(channel, "find ($user|$item) $user: display users bank, $item: displays item price")
        sendmsg(channel, "(listitems|li): list's all items (in theory)")
        sendmsg(channel, "(addbank|addmonies|bank+=|addfunds|addmoney|add): add money to your bank")
        sendmsg(channel, "source: will give github source link")
        sendmsg(channel, "you may /query bb and use zb: commands like normal")

    elif command == "buy" or command == "purchase":
        # arglist is the list of things the person wants to buy, we concat them
        # into one string, and send that string as a single argument
        purchase_item = concat_list(arglist)

        # One "special" persons case for one person who feels their username should not be their zuulname too ;)
        # if str(usern) == str("zaalatta"):
        # usern = "zolo"

        # a bunch of special purchase cases
        soda_list = ("coke", "pepsi", "sprite", "drpepper", "dr.pepper", "can",
                     "soda", "mtdew", "mt.dew", "mountain dew")

        if purchase_item.lower() in soda_list:
            purchase_item = "Canned Beverage"

        if purchase_item.lower() == "cheese":
            purchase_item = "String Cheese"

        if purchase_item.lower() == "rice krispies":
            purchase_item = "Rice Krispies Bar"

        if purchase_item.lower() == "granola":
            purchase_item = "Granola Bar"
        # End special cases

        booluser, username, userbank = finduser(usern, channel, quiet=True)
        boolitem, itemname, itemcost = finditem(purchase_item, channel, quiet=True)
        if booluser is False:
            sendmsg(channel, "that user was not found")
        if boolitem is False:
            sendmsg(channel, "that item was not found!")
        if booluser is True and boolitem is True and\
           purchaseitem(usern, purchase_item, channel) is True:
            boolusernew, usernamenew, userbanknew = finduser(usern, channel, quiet=True)
            sendmsg(channel, "user: %s, %s, purchased: %s, %s and now has: %s left" % (username,
                                                                                       userbank,
                                                                                       itemname,
                                                                                       itemcost,
                                                                                       userbanknew))

    elif command == "find":
        print "general find was called"
        find_me = concat_list(arglist)  # get the item/user argument
        # set boolitem to true if found, false if not
        boolitem, itemname, itemcost = finditem(find_me, channel)
        if boolitem is False:
            # set booluser to true if found, false if not
            booluser, username, userbank = finduser(find_me, channel)
            if booluser is False:
                sendmsg(channel, "did not find, please check spelling (check zuul.cat.pdx.edu/newzuul for list)")

    elif command == "finduser" or command == "fus" or command == "finditem" or command == "fit":
        sendmsg(channel, "command %s is defunct, please use 'find' for all searches from now on" % command)

    elif command == "listitems" or command == "li" or command == "inventory":
        print "listitems was called"
        payload = {"name": arglist[0], "item": arglist[1]}
        r = requests.post(weblocation + "/newzuul/v1/listall/", data=payload)
        if r.status_code == 200:
            return_dict = j.loads(r.text)
            for item in return_dict:
                if item == "success":
                    continue
                else:
                    sendmsg(usern, "%s: %s" % (str(item), str(return_dict[item])))
        else:
            sendmsg(channel, "benzer, halp! r.status_code was %s" % str(r.status_code))

    elif command == "addbank" or command == "addfunds" or command == "addmonies" or command == "addmoney" or command == "bank+=" or command == "add":
        print "addbank was called"
        ammount = concat_list(arglist)  # get the item/user argument

        booluser0, username0, userbank0 = finduser(usern, channel, quiet=True)
        boolbank = addtobank(usern, ammount, channel)
        if boolbank is not False:
            booluser1, username1, userbank1 = finduser(usern, channel, quiet=True)
            sendmsg(channel, "user: " + str(usern) + " had bank: $" + str(userbank0) + " and added $" + str(ammount) + " and now has: $" + str(userbank1))

        # set boolitem to true if found, false if not

    elif command == "source" or command == "Source" or command == "-source" or command == "--source":
        print "source command called"
        source = "https://github.com/BrianBreniser/BenzerBot"
        sendmsg(channel, "Source code is: " + source)

    elif command == "gift":
        print "gift command called"

# --- End Zuulbot's functions --- #

# --- Start Benzerbot's functions --- #


def benzerbot(user, channel, command, arglist):
    """Number of commands for benzerbot."""
    print "benzerbot was called"

    if command == "hello" or command == "hi" or command == "hola" or command == "oi" or command == "hey":
        print "hello was called"
        sendmsg(channel, "hola %s" % user)

    elif command == "join":
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

    elif command == "addadmin":
        print "newadmin was called"
        anadmin = isadmin(user)
        if anadmin == '1':
            sendmsg(channel, "okay, %s is now an admin" % arglist[0])
            addadmin(arglist[0])
        elif anadmin == '0':
            sendmsg(channel, "But, I don't take orders from %s" % user)
        else:
            sendmsg(channel, "benzer, help, I got %s" % isadmin)

    elif command == "help" or command == "halp" or command == "derp" or command == "wat" or command == "what":
        print "help was called"
        sendmsg(channel, "Commands:")
        sendmsg(channel, "(hello|hi|hey|oi|hola)")
        sendmsg(channel, "join $channel")
        sendmsg(channel, "join $channel permanently")
        sendmsg(channel, "you can also pm: bb ")
        sendmsg(channel, "you can also address:")
        sendmsg(channel, "(zuulbot|zb): help")
        sendmsg(channel, "(bdbot|bd): help")
        sendmsg(channel, "source")

    elif command == "pme":
        print "pme was called"
        sendmsg(user, "you told me to PM you: %s" % arglist[0])

# --- End Benzerbot's functions --- #

# --- Start infinite loop to do bot things --- #


def main():
    """Our infinite loop of catching user input."""
    while 1:  # Be careful with these! it might send you to an infinite loop
        ircmsg = ircsock.recv(2048)  # receive data from the server
        ircmsg = ircmsg.strip('\n\r')  # removing any unnecessary linebreaks.
        print ircmsg  # Here we print what's coming from the server

        # imediatly PONG
        if ircmsg.find("PING") != -1:  # PONG on server PING
            pong()

        # Kicks if somebody talks
        if ircmsg.find("PRIVMSG"):
            splitircmsg = ircmsg.split() + [" ", " ", " "]  # cuts stringf
            user = str(splitircmsg[0].split("!")[0]).replace(":", "")  # user
            channel = str(splitircmsg[2]).lower()  # the channel

            if channel == "bb" or channel == "zuulbot" or channel == "bdbot":  # if channel is pm window
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

# --- Start multiprocess threading --- #

if __name__ == '__main__':
    main()

# --- End multiprocess threading --- #
