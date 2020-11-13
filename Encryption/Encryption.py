#!/usr/bin/python3

import string,sys

#start of class
class EncryptionSub:
    
    #all the characters to cipher plus special
    characterSet = string.ascii_lowercase + string.ascii_uppercase + string.digits + " "+ string.punctuation

    def encrypt(self, msg, key, leftshift=False):
        
        key = (key%94) +1 #keeping key in [1, 256]
        
        if leftshift:
            key = -1*key
    
        #creating a hashtable mapping all the characters to their new cipher value according to given key.
        hashtable = str.maketrans(self.characterSet, self.characterSet[key:] + self.characterSet[:key])
        
        cipher = msg.translate(hashtable)
        
        return cipher
        
    def decrypt(self, encryptmsg, key, leftshift=False):
        
        key = (key%94) +1 #keeping key in [1, 256]
        
  
        total = len(self.characterSet)
        key = total - key
        
        if leftshift:
            key = -1*key
        
        #creating a hashtable mapping all the characters to their new cipher value according to given key.
        hashtable = str.maketrans(self.characterSet, self.characterSet[key:] + self.characterSet[:key])
        
        plaintext = encryptmsg.translate(hashtable)
        
        return plaintext
        
# end of the class

#start of class
class EncryptionTran:
    
    key = 0

    def __init__(self, key):
        self.key = key
           
        
    def encrypt(self, msg):
        msg =  " msg should be encrypted by Trans here"
        return msg
    
    def decrypt(self, encryptmsg):
        encryptmsg = " msg should be decrypted by Trans here"
        return encryptmsg
    
# end of the class


#begin of main
if(__name__ == "__main__"):
    #to handle commands if executed from CLI.
    
    
    if len(sys.argv) > 1:
        
        try:    
            
            correctInput = sys.argv[1].upper() in "ST"
            correctInput = sys.argv[2].upper() in "ED"
            correctInput = sys.argv[3] in "0123456789"
            correctInput = sys.argv[4].upper() not in " "
        except:
            print("Error: format is Encryption.py -[S/T] -[E/D] -key -filepath -shift[R/L]")
            exit(1)
        if correctInput:
            
            SubTan = sys.argv[1].replace("-","").upper()
            mode = sys.argv[2].replace("-","").upper()
            key = int(sys.argv[3].replace("-",""))
            filepath = sys.argv[4].replace("-","")
            if len(sys.argv) > 5:
                shift = sys.argv[5].replace("-","").upper() =="L"
            
        else:
            
            print("Error: format is Encryption.py -[S/T] -[E/D] -key -filepath -shift[R/L]")
            exit(1)
    else:
        
        print("Hello user, please give me the file path")
        filepath = input("file path : ")
        
        print("What type of algorithm do you wish to use ?")
        SubTan = input("S or T : ")
        
        print("What do you want to encypt this file or decrypt it ?")
        mode = input("E or D : ")
        
        print("Provide me with a key, kind soul.")
        key = int(input("key : "))
    
    try:
        file_object  = open(filepath, "r+")
    
    except Exception as e: print(e)
        
    msg = ""
    
    for line in file_object:
        msg += line
    

    
    
    #print("the msg is " + msg)
    
    if(SubTan == "S"):
        msgHandler = EncryptionSub()
        if len(sys.argv) < 5:
            print("Do you want to shift to the left or to the right ? ")
            shift = bool(input("R or L, default is right : ") =="L")
        if(mode == "E"):
            msg = msgHandler.encrypt(msg, key, shift)
            
        elif (mode == "D"):
            msg = msgHandler.decrypt(msg, key, shift)
            
    elif(SubTan == "T"):
        msgHandler = EncryptionTran()
        
        if(mode == "E"):
            msg = msgHandler.encrypt(msg)
            
        elif (mode == "D"):
            msg = msgHandler.decrypt(msg)
    

    file_object.seek(0)
    file_object.writelines(msg)
    file_object.truncate()
    file_object.close()
    
    