#!/usr/bin/python
from signal import SIGINT
import socket
import select
import sys
import hashlib
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA1, HMAC


def calculate_sha1(strValue):
    sha1Hash = SHA1.new()
    testBytes = strValue.encode()
    sha1Hash.update(testBytes)
    return sha1Hash




# sets up the socket info
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if len(sys.argv) < 2 or len(sys.argv) > 8: # handles erroneous user input
    print("Incorrect Input")
    sys.exit()

# Handles server side 
if sys.argv[1] == '-s':

    # implies no port was given, binds the port to 9999
    if len(sys.argv) != 7: 
        portNum = 9999
        confKey = str(sys.argv[3])
        authKey = str(sys.argv[5])

    # implies port was given, binds the port to user input
    else:
        portNum = int(sys.argv[2])
        confKey = str(sys.argv[4])
        authKey = str(sys.argv[6])

    confHash = calculate_sha1(confKey) # calculates hash for confkey
    authHash = calculate_sha1(authKey) # calculates hash for authkey

    trimmedConf = confHash.hexdigest()[:-8] # trims confkey to 128 bits string
    trimmedAuth = authHash.hexdigest()[:-8] # trims authkey to 128 bits string

    confKey128 = trimmedConf.encode() # convets the 128 bit string to bytes
    authKey128 = trimmedAuth.encode() # convets the 128 bit string to bytes

    print(confKey128)
    print(authKey128)

    #AES.new(strConf, AES.MODE_CBC, get_random_bytes(16))   



    # server.bind(('127.0.0.1', portNum))
    # server.listen(1)
    # connection, address = server.accept()

    # while True: 
  
    #     # maintains a list of possible input streams 
    #     read_options = [sys.stdin, connection] 

    #     r, w, e = select.select(read_options,[],[]) 

    #     for sockets in r: 

    #         # Handles server message sending
    #         if sockets is connection: 
    #             encodedMessage = sockets.recv(1024)
    #             message = encodedMessage.decode()
    #             #print('<{}>{}'.format(address[0], message))
    #             if len(message) == 0:
    #                 sys.exit()  
    #             print(message)

    #         # Handles client message 
    #         else: 
    #             unencodedMessage = sys.stdin.readline() # gets the user input including the escape character
    #             message = unencodedMessage.encode()
    #             connection.send(message) 

    # connection.close()

    

# Handles client side
elif sys.argv[1] == '-c':
    #print('This terminal is running the client-side')
    hostname = sys.argv[2]

    # implies no port was given, binds the port to 9999
    if len(sys.argv) != 8:
        portNum = 9999
        confKey = str(sys.argv[4])
        authKey = str(sys.argv[6])

    # implies port was given, binds the port to user input
    else:
        portNum = int(sys.argv[3])
        confKey = str(sys.argv[5])
        authKey = str(sys.argv[7])

    # server.connect((hostname, portNum))

    # while True: 
  
    #     # maintains a list of possible input streams 
    #     read_options = [sys.stdin, server] 

    #     r, w, e = select.select(read_options,[],[]) 
  
    #     for sockets in r: 

    #         # Handles server message sending
    #         if sockets is server: 
    #             encodedMessage = sockets.recv(1024)
    #             message = encodedMessage.decode()
    #             #print('<Server>{}'.format(message))
    #             if len(message) == 0:
    #                 sys.exit() 
    #             print(message)

    #         # Handles client message 
    #         else: 
    #             unencodedMessage = sys.stdin.readline() # gets the user input including the escape character
    #             message = unencodedMessage.encode()
    #             server.send(message)  


# Errors
else:
    #print('Error: did not specify where to run')
    sys.exit()

server.close()