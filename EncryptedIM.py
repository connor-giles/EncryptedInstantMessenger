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

def encrypt_CBC(encryptedCKey, messageToSend, HMAC):
    IV = get_random_bytes(16) # creates a random Initialization vector
    encryptionCalculator = AES.new(encryptedCKey, AES.MODE_CBC, IV)
    cipherText = encryptionCalculator.encrypt(pad(messageToSend.encode(), AES.block_size))
    cipherTextWithExtras = HMAC + IV + cipherText
    return cipherTextWithExtras

def decrypt_CBC(encryptedCKey, encryptedMessage, origAuthKey):
    # gets the HMAC sent from the sender
    sentHMAC = encryptedMessage[:32].decode() 

    # gets rest of message and parses IV from it 
    sentMessageAndIV = encryptedMessage[32:]
    sentIV = sentMessageAndIV[:16]

    # gets the encrypted message itself
    sentMessage = sentMessageAndIV[16:]

    # creates and AES object to decrypt
    cipherText = AES.new(encryptedCKey, AES.MODE_CBC, sentIV)
    plainText = unpad(cipherText.decrypt(sentMessage), AES.block_size)
    plainText = plainText.decode() # returns it back to a string from bytes

    # calculate HMAC and compare to the HMAC sent
    personalHMAC = encrypt_HMAC(origAuthKey, plainText).decode()

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
                message = sockets.recv(1024)

                if len(message) == 0:
                    sys.exit() 

                messageDecrypted = decrypt_CBC(encryptedConfKey, message, authKey)
                print(messageDecrypted)

            # Handles client message 
            else: 
                userMessage = sys.stdin.readline() # gets the user input including the escape character
                encryptedHMAC = encrypt_HMAC(authKey, userMessage)
                cipherText = encrypt_CBC(encryptedConfKey, userMessage, encryptedHMAC)
                connection.send(cipherText) 

    connection.close()

    

# Handles client side
elif sys.argv[1] == '-c':

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

    encryptedConfKey = encrypt_confKey_128(confKey)
    server.connect((hostname, portNum))

    while True: 
  
        # maintains a list of possible input streams 
        read_options = [sys.stdin, server] 

        r, w, e = select.select(read_options,[],[]) 
  
        for sockets in r: 

            # Handles server message sending
            if sockets is server: 
                message = sockets.recv(1024)

                if len(message) == 0:
                    sys.exit() 

                messageDecrypted = decrypt_CBC(encryptedConfKey, message, authKey)
                print(messageDecrypted)

            # Handles client message 
            else: 
                userMessage = sys.stdin.readline() # gets the user input including the escape character
                encryptedHMAC = encrypt_HMAC(authKey, userMessage)
                cipherText = encrypt_CBC(encryptedConfKey, userMessage, encryptedHMAC)
                server.send(cipherText) 


# Errors
else:
    sys.exit()

server.close()