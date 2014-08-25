#!/usr/bin/python
import socket 
import time
# Some basic variables used to configure the bot        
server="irc.cat.pdx.edu" # Server
channel="#benzertest" # Channel
botnick="benzerbot" # Your bots nick


def ping():
  ircsock.send("PONG :pingis\n")  

def sendmsg(chan , msg): # This is the send message function, it simply sends messages to the channel.
  ircsock.send("PRIVMSG "+ chan +" :"+ msg +"\n") 

def joinchan(chan): # This function is used to join channels.
  ircsock.send("JOIN "+ chan +"\n")

def hello(): # This function responds to a user that inputs "Hello Mybot"
  ircsock.send("PRIVMSG "+ channel +" :Shut up...\n")

def punch(): 
  ircsock.send("PRIVMSG "+ channel + " :No. He's a nice guy!\n")


ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667)) # Here we connect to the server using the port 6667
ircsock.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :This bot is a result of a tutoral covered on http://shellium.org/wiki.\n") # user authentication
ircsock.send("NICK "+ botnick +"\n") # here we actually assign the nick to the bot

joinchan(channel) # Join the channel using the functions we previously defined

while 1: # Be careful with these! it might send you to an infinite loop
  ircmsg = ircsock.recv(2048) # receive data from the server
  ircmsg = ircmsg.strip('\n\r') # removing any unnecessary linebreaks.
  print(ircmsg) # Here we print what's coming from the server
       
  if ircmsg.find(":"+botnick+": punch") != -1: # If we can find "Hello slimbot" it will call the function hello()
     punch() 

  if ircmsg.find("PING :") != -1: # if the server pings us then we've got to respond!
     ping()

         


