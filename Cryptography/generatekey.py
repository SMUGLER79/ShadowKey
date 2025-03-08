from cryptography.fernet import Fernet

key = Fernet. generate_key()

file = open("encryptionKey.txt", 'wb')
file.write(key)
file.close()