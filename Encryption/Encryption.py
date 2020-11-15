#!/usr/bin/python3

import string,sys
from collections import deque
import math

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
           
        
    def encrypt(self, msg, key):
        if key < 10:
            return;
        
        lsmsg = list(msg.replace("\n", ""))
        lskey= list(str(key))
        lenKey = int(math.log10(key))+1
        
        while len(lsmsg) % lenKey != 0:
            lsmsg.append(" ")
        
        dq = deque(lsmsg)


        encryptedMsg = []
        first = 0

        for i in range(len(dq)):
            
            if i%lenKey == 0:
                if first > 0:
                    for k in range(lenKey):
                        dq.popleft()
                    
                first +=1
                
            digit = lskey[i%lenKey]
            char = dq[(int(digit) - 1)]
            encryptedMsg.append(char)
            
        
        return encryptedMsg
    
    def decrypt(self, encryptmsg, key):
        if key < 10:
            return;
        
        lsmsg = list(encryptmsg)
        lskey= list(str(key))
        lenKey = int(math.log10(key))+1
        
        while len(lsmsg) % lenKey != 0:
            lsmsg.append(" ")
        
        dq = deque(lsmsg)

        plainttext = ["" for i in range(len(dq))]
        first = 0
        offset = 0
        i=0
        
        while dq:
            
            if i%lenKey == 0:
                if first > 0:
                    if i%lenKey == 0:
                        offset +=lenKey
                        i=0
                    for k in range(lenKey):
                        dq.popleft()
                    
                first +=1
            if dq:
                   
                digit = lskey[i%lenKey]
                char = dq[i]
                plainttext[int(digit)-1+offset] = char
                i+=1 
        
        return plainttext
    
# end of the class


#start of main
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
        
        print("Hello kind soul,\nJust letting you know that you can execute me directly from the terminal using the command: \nEncryption.py -[S/T] -[E/D] -key -filepath -shift[R/L] (shift is optional and only for subsitution)\nBut since we're here, please give me the file path")
        filepath = input("file path : ")
        
        print("What type of algorithm do you wish to use ?")
        SubTan = input("S or T : ")
        
        print("What do you want to encypt this file or decrypt it ?")
        mode = input("E or D : ")
        
        print("Provide me with a key, kind soul. \nThe key for subsitution must be between 1-256. \nThe key for Transposition must be something like 4132 where each number corresponds to a position.")
        key = int(input("key : "))
    
    try:
        file_object  = open(filepath, "r+")
    
    except Exception as e: print(e)
        
    msg = ""
    
    for line in file_object:
        msg += line
    

    
    
    #print("the msg is " + msg)
    
    if(SubTan.lower() == "s"):
        msgHandler = EncryptionSub()
        if len(sys.argv) < 5:
            print("Do you want to shift to the left or to the right ? ")
            shift = bool(input("R or L, default is right : ") =="L")
        if(mode.lower() == "e"):
            msg = msgHandler.encrypt(msg, key, shift)
            
        elif (mode.lower() == "d"):
            msg = msgHandler.decrypt(msg, key, shift)
        else:
            print("Error: unknown mode (E/D).")
            
    elif(SubTan.lower() == "t"):
        msgHandler = EncryptionTran()
        
        if(mode.lower() == "e"):
            msg = msgHandler.encrypt(msg,key)
            
        elif (mode.lower() == "d"):
            msg = msgHandler.decrypt(msg,key)
        else:
            print("Error: unknown mode (E/D).")
    else:
        print("Error: unknown Encryption Algorithm.")
        
    file_object.seek(0)
    file_object.writelines(msg)
    file_object.truncate()
    file_object.close()
    print("DONE !")
    
    