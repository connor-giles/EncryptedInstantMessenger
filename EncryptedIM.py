#!/usr/bin/python
from signal import SIGINT
import socket
import select
import sys
import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA1, HMAC
from Crypto.Util.Padding import pad, unpad

# calculates 128 bit hash for confkey
def encrypt_confKey_128(stringConfKey):
    sha1Hash = SHA1.new()
    byteString = stringConfKey.encode()
    sha1Hash.update(byteString)
    sha1Hash = sha1Hash.hexdigest()[:-8] # trims confkey to 128 bits string
    return sha1Hash.encode()

# encrypts and trims to get appropriate HMAC
def encrypt_HMAC(stringAuthKey, message):
    authHMAC = HMAC.new(stringAuthKey.encode(), message.encode(), SHA1)
    authHMAC = authHMAC.hexdigest()[:-8] # trims to 128 bits
    return authHMAC.encode()

# def decrypt_HMAC():
#     return

def encrypt_CBC(encryptedCKey, messageToSend, HMAC):
    IV = get_random_bytes(16) # creates a random Initialization vector
    encryptionCalculator = AES.new(encryptedCKey, AES.MODE_CBC, IV)
    cipherText = encryptionCalculator.encrypt(pad(messageToSend.encode(), AES.block_size))
    # print("Original CipherText: {}".format(cipherText))
    # print("Original IV: {}".format(IV))
    cipherTextWithExtras = HMAC + IV + cipherText
    return cipherTextWithExtras

def decrypt_CBC(encryptedCKey, encryptedMessage, origAuthKey):
    # gets the HMAC sent from the sender
    sentHMAC = encryptedMessage[:32].decode() 

    # gets rest of message and parses IV from it 
    sentMessageAndIV = encryptedMessage[32:]
    sentIV = sentMessageAndIV[:16]
    print("Sent IV: {}".format(sentIV))

    # gets the encrypted message itself
    sentMessage = sentMessageAndIV[16:]
    print("Sent Message: {}".format(sentMessage))

    # creates and AES object to decrypt
    cipherText = AES.new(encryptedCKey, AES.MODE_CBC, sentIV)
    plainText = unpad(cipherText.decrypt(sentMessage), AES.block_size)
    plainText = plainText.decode() # returns it back to a string from bytes

    # calculate HMAC and compare to the HMAC sent
    personalHMAC = encrypt_HMAC(origAuthKey, plainText).decode()
    print("Sent HMAC: {}".format(sentHMAC))
    print("Personal HMAC: {}".format(personalHMAC))

    if(personalHMAC != sentHMAC):
        print("The HMAC's do not match!")
        sys.exit()

    return plainText





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

    encryptedConfKey = encrypt_confKey_128(confKey)
    encryptedHMAC = encrypt_HMAC(authKey, "Test message")
    cipherText = encrypt_CBC(encryptedConfKey, "Test message", encryptedHMAC)

    pText = decrypt_CBC(encryptedConfKey, cipherText, authKey)
    print("PlainText: {}".format(pText))

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
    sys.exit()

server.close()