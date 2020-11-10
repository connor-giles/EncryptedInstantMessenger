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
from Crypto.Util.Padding import pad

# calculates 128 bit hash for confkey
def encrypt_confKey_128(stringConfKey):
    sha1Hash = SHA1.new()
    byteString = stringConfKey.encode()
    sha1Hash.update(byteString)
    sha1Hash = sha1Hash.hexdigest()[:-8] # trims confkey to 128 bits string
    return sha1Hash.encode()

def encrypt_HMAC_128(stringAuthKey):
    authHMAC = HMAC.new(stringAuthKey.encode(), b'hello', SHA1)
    authHMAC = authHMAC.hexdigest()[:-8] # trims to 128 bits
    return authHMAC.encode()




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


    encryptedConKey = encrypt_confKey_128(confKey)

    print("128 bit confKey: {}".format(encryptedConKey))
  

    encryptedHMAC = encrypt_HMAC_128(authKey)

    print("128 bit HMAC: {}".format(encryptedHMAC))
    
    # encryptionCalculator = AES.new(confKey128, AES.MODE_CBC, get_random_bytes(16))
    # cipherText = encryptionCalculator.encrypt(pad(b"secret message", AES.block_size))

    # print(cipherText)



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