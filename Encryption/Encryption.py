#!/usr/bin/python3

import string,sys
from collections import deque
import math

#start of class
class EncryptionSub:
    
    #variable to store all the characters to be ciphered plus special characters.
    characterSet = string.ascii_lowercase + string.ascii_uppercase + string.digits + " "+ string.punctuation
    #this will be used by the caesar cipher.
    
    def encrypt(self, msg, key, leftshift=False):
        
        #making sure the key is only 8bits, i.e between 1 ... 256
        #since we're using caesar here, the keys are only between 1..95
        key = (key%94) +1 #keeping key in [1, 95]
        
        #if the user demands left shift, we take the negative value of the key.
        if leftshift:
            key = -1*key
        
        #the str.maketrans is a method that is part of the string object methods
        #that creates a translation table which resembles a hashtables that has all the alphabet
        #which is self.characterSet as keys and the values are the translated alphabet in the other side.
        #self.characterSet[Key:] slices the charcters from the index [key] to the end of the characters, while 
        #the other one slices it from the beginning all the way to the index [key].
        #adding these two slices creates a translated alphabet according to key, 
        #which is what the caesar cipher does. 
        hashtable = str.maketrans(self.characterSet, self.characterSet[key:] + self.characterSet[:key])
        
        #this method uses the generated hashtable to translate each letter to it's new ciphered value.
        cipher = msg.translate(hashtable)
        
        return cipher
        
    def decrypt(self, encryptmsg, key, leftshift=False):
        
        #making sure the key is only 8bits, i.e between 1 ... 256
        #since we're using caesar here, the keys are only between 1..95
        key = (key%94) +1 #keeping key in [1, 95]
        
        #calculating the number of elements in our characterSet.
        total = len(self.characterSet)
        #updating the key by getting the reminder of the total minus the key,
        #this will give us a value that will slice the characterSet back to its
        #original values.
        key = total - key
        
        #if the user had encrypted with left shift, we'll decrypt with it as well,
        #as the shift will affect the direction of the slicing of the string.
        if leftshift:
            key = -1*key
        
        #same as before, however now the hashtable will have values that corresponds 
        #to their actual plaintext values.
        hashtable = str.maketrans(self.characterSet, self.characterSet[key:] + self.characterSet[:key])
        
        #using the generated hashtable to decrypt the message.
        plaintext = encryptmsg.translate(hashtable)
        
        return plaintext
        
# end of the class

#start of class
class EncryptionTran:
           
    #using simple transposition.
        
    def encrypt(self, msg, key):
    
        #since the key for the transposition method is a sequence of columns,
        #the key must be at least > 10 for this to work.
        #it must also be a permutation that starts from 1.
        #examples of valid keys : 4132, 21, 53124 ... etc.
        if key < 10:
            return;
        
        #first of all, removing the new line symbol from the end of the file.
        #then converting the string message to a list.
        lsmsg = list(msg.replace("\n", ""))
        #converting the key to a string, then to a list so we can reference
        #the columns.
        lskey= list(str(key))
        #calculating the length of the key using the math.log10 method as it's
        #O(logN).
        lenKey = int(math.log10(key))+1
        
        #if the length of the message is not a multiple of the length of the key,
        #we add a some spaces to the end of the message so that we can divide the
        #message by the key length and always get a whole number.
        while len(lsmsg) % lenKey != 0:
            lsmsg.append(" ")
        
        #creating a deque using the message list.
        #deques in python are essentially two-way queues or simply put
        # a double linked list.
        dq = deque(lsmsg)

        #creating an empty list for  the encrypted message.
        encryptedMsg = []
        #a counter.
        first = 0
        
        #for every element in the queue
        for i in range(len(dq)):
            
            #if we are at an index that is a multiple of the key length.
            #this means we arrived to a new chunk of the message that we can apply
            #the key to.
            if i%lenKey == 0:
                #if we're on the first chunk, skip.
                if first > 0:
                    #if we're on every other chunk
                    #we're going to pop the last chunk out of the deque.
                    for k in range(lenKey):
                        dq.popleft()
                #increment first so that it applies to every chunk except the first.
                first +=1
                
            #extracting the column number from the key list.
            digit = lskey[i%lenKey]
            #getting the character from that column to replace it with the current
            #index i character.
            char = dq[(int(digit) - 1)]
            #adding the character acquired from the column number to the encrypted
            #message.
            encryptedMsg.append(char)
            
        
        return encryptedMsg
    
    def decrypt(self, encryptmsg, key):
        #since the key for the transposition method is a sequence of columns,
        #the key must be at least > 10 for this to work.
        #it must also be a permutation that starts from 1.
        #examples of valid keys : 4132, 21, 53124 ... etc.        
        if key < 10:
            return;
        #converting the cipher to a list.
        lsmsg = list(encryptmsg)
        #converting the key to a list.
        lskey= list(str(key))
        #getting the size of the key.
        lenKey = int(math.log10(key))+1
        
        #if the cipher's length is not a mulitple of the key length, make it so.
        while len(lsmsg) % lenKey != 0:
            lsmsg.append(" ")
        
        #converting the cipher list to a deque.
        dq = deque(lsmsg)
        
        #creating a plaint text list that has " " in all it's cells.
        #it's the same size as the encrypted message.
        plainttext = ["" for i in range(len(dq))]
        
        #counter variables.
        first = 0
        offset = 0
        i=0
        
        #while the deque is not empty... yes this is how python handles it.
        while dq:
            #if the index is a multiple of the key length, we arrived at a new chunk
            if i%lenKey == 0:
                #if we're not in the first chunk.
                if first > 0:
                    if i%lenKey == 0:
                        #adding the length of the key to the offset so that
                        #we move ahead to the next chunk.
                        offset +=lenKey
                        #resetting the index to 0 because we already popped
                        #the last chunk that was decrypted.
                        i=0
                    #pop the last chunk that was decrypted.
                    for k in range(lenKey):
                        dq.popleft()
                    
                first +=1
            #if deque is not empty    
            if dq:
                #get the column number from the key.   
                digit = lskey[i%lenKey]
                #get the character from that column.
                char = dq[i]
                #restore that character to it's original position and place it
                #in the plaint text list.
                plainttext[int(digit)-1+offset] = char
                #increment index.
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
                shift = sys.argv[5].replace("-","").upper() in "L"
            else:
                shift = False
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
    
    