#!/usr/bin/python
from signal import SIGINT
import socket
import select
import sys
#from Crypto.Cipher import AES
#from Crypto.Random import get_random_bytes

# sets up the socket info
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if len(sys.argv) < 2 and len(sys.argv) > 4: # handles erroneous user input
    print
    sys.exit()

# Handles server side 
if sys.argv[1] == '-s':
    #print('This terminal is running the server-side')
    if len(sys.argv) != 3:
        # bind the port to 9999
        portNum = 9999

    else:
        # bind the port to user input
        portNum = int(sys.argv[2])

    server.bind(('127.0.0.1', portNum))
    server.listen(1)
    connection, address = server.accept()

    while True: 
  
        # maintains a list of possible input streams 
        read_options = [sys.stdin, connection] 

        r, w, e = select.select(read_options,[],[]) 

        for sockets in r: 

            # Handles server message sending
            if sockets is connection: 
                encodedMessage = sockets.recv(1024)
                message = encodedMessage.decode()
                #print('<{}>{}'.format(address[0], message))
                if len(message) == 0:
                    sys.exit()  
                print(message)

            # Handles client message 
            else: 
                unencodedMessage = sys.stdin.readline() # gets the user input including the escape character
                message = unencodedMessage.encode()
                connection.send(message) 

    connection.close()

    

# Handles client side
elif sys.argv[1] == '-c':
    #print('This terminal is running the client-side')
    hostname = sys.argv[2]

    if len(sys.argv) != 4:
        # bind the port to 9999
        portNum = 9999

    else:
        # bind the port to user input
        portNum = int(sys.argv[3])

    server.connect((hostname, portNum))

    while True: 
  
        # maintains a list of possible input streams 
        read_options = [sys.stdin, server] 

        r, w, e = select.select(read_options,[],[]) 
  
        for sockets in r: 

            # Handles server message sending
            if sockets is server: 
                encodedMessage = sockets.recv(1024)
                message = encodedMessage.decode()
                #print('<Server>{}'.format(message))
                if len(message) == 0:
                    sys.exit() 
                print(message)

            # Handles client message 
            else: 
                unencodedMessage = sys.stdin.readline() # gets the user input including the escape character
                message = unencodedMessage.encode()
                server.send(message)  


# Errors
else:
    #print('Error: did not specify where to run')
    sys.exit()

server.close()