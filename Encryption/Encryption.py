

#this function is shamelessly taken from " https://stackoverflow.com/questions/11122291/how-to-find-char-in-string-and-get-all-the-indexes#11122355 " 
def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

def insert_spaces(text, s_range):
        return ' '.join(text[start:end] for start, end in 
                        zip([0] + s_range, s_range + [len(text)])).strip()

#start of class
class EncryptionSub:
    
    default = ["playf", "irexm", "bcdgh", "knoqs", "tuvwz"]
    key_matrix = []
    preparedMsg = []
    seenInd = []
    spaceInd = []
    key = 0

    def __init__(self, key):
        self.key = key % 257 #keeping key in [0 , 256]
           
    
    def _shiftmatrix(self):
        
        tmp = key % 5
        
        for row in self.default:
        
            tmpstr = row[tmp:] + row[:tmp]
            self.key_matrix.append(tmpstr)
            tmp = (tmp) % 5

        #print(self.key_matrix)
    
    def _prepareMsg(self, msg):
        
        i = 0
        while i < len(msg)-1:
            a = msg[i]
            b = ""
            
            if (i+1) == len(msg): #we arrived to the last letter.
                b = "x"
            else:
                b = msg[i+1]
            '''
            if a in ".;',!?@\":&":
                self.preparedMsg.append("x" + b)
                i += 2
            elif b in ".;',!?@\":&":
                self.preparedMsg.append(a + "x")
                i += 2
            else:
            '''
            self.preparedMsg.append(a + b)
            i += 2
    
    def _replaceRows(self,encyptedmsg):
        
        for row in self.key_matrix:
            #print("Row is : " + row)
            for pairInd in range(len(self.preparedMsg)):
                pair = self.preparedMsg[pairInd]
                
                if pair[0] in row and pair[1] in row:
                    indx1 = row.find(pair[0])
                    indx2 = row.find(pair[1])
                    
                    #print("first letter is " + pair[0])
                    #print("first letter is " + pair[1])
                    #print("first indx " + str(indx1))
                    #print("second indx " + str(indx2))
                    
                    a = row[(indx1 + 1) % 5]
                    b = row[(indx2 + 1) % 5]
                    
                    encyptedmsg[pairInd] = a+b
                    self.seenInd.append(pairInd)
                    
                     
    
    def _restoreRows(self,msg):
        
        for row in self.key_matrix:
            #print("Row is : " + row)
            for pairInd in range(len(self.preparedMsg)):
                pair = self.preparedMsg[pairInd]
                
                if pair[0] in row and pair[1] in row:
                    indx1 = row.find(pair[0])
                    indx2 = row.find(pair[1])
                    
                    #print("first letter is " + pair[0])
                    #print("first letter is " + pair[1])
                    #print("first indx " + str(indx1))
                    #print("second indx " + str(indx2))
                    
                    a = row[(indx1 + 4) % 5]
                    b = row[(indx2 + 4) % 5]
                    
                    msg[pairInd] = a+b
                    self.seenInd.append(pairInd)
                  
    def _replaceCols(self,encyptedmsg):
        
        for row in range(5):
            
            column = "".join(self.key_matrix[i][row] for i in range(5))
            
            for pairInd in range(len(self.preparedMsg)):
                pair = self.preparedMsg[pairInd]
                
                if pair[0] in column and pair[1] in column:
                    
                    indx1 = column.find(pair[0])
                    indx2 = column.find(pair[1])
                        
                    a = column[(indx1 + 1) % 5]
                    b = column[(indx2 + 1) % 5]
                    
                    if pairInd not in self.seenInd:
                        encyptedmsg[pairInd] = a+b
                        self.seenInd.append(pairInd)
                    
    
    def _restoreCols(self, msg):
        
        for row in range(5):
            
            column = "".join(self.key_matrix[i][row] for i in range(5))
            
            for pairInd in range(len(self.preparedMsg)):
                pair = self.preparedMsg[pairInd]
                if pair[0] in column and pair[1] in column:
                    
                    indx1 = column.find(pair[0])
                    indx2 = column.find(pair[1])
                        
                    a = column[(indx1 + 4) % 5]
                    b = column[(indx2 + 4) % 5]
                    
                    if pairInd not in self.seenInd:
                        msg[pairInd] = a+b
                        self.seenInd.append(pairInd)    
                                   
    def _replaceBox(self,encyptedmsg):
        x0=0 
        y0=0 
        x1=0 
        y1=0
        
        for pairInd in range(len(self.preparedMsg)):
            
            pair = self.preparedMsg[pairInd]
            
            for rowInd in range(5):
                row = self.key_matrix[rowInd]
                
                
                if pair[0] in row:
                    x0 = rowInd
                    y0 = row.find(pair[0])
                if pair[1] in row:
                    x1 = rowInd
                    y1 = row.find(pair[1])
                
                if pairInd not in self.seenInd:
                    encyptedmsg[pairInd] = self.key_matrix[x0][y1] + self.key_matrix[x1][y0]
                
    def _restoreBox(self, msg):
        x0=0 
        y0=0 
        x1=0 
        y1=0
        
        for pairInd in range(len(self.preparedMsg)):
            
            pair = self.preparedMsg[pairInd]
            
            for rowInd in range(5):
                row = self.key_matrix[rowInd]
                
                
                if pair[0] in row:
                    x0 = rowInd
                    y0 = row.find(pair[0])
                if pair[1] in row:
                    x1 = rowInd
                    y1 = row.find(pair[1])
                if pairInd not in self.seenInd:
                    msg[pairInd] = self.key_matrix[x0][y1] + self.key_matrix[x1][y0]
                    #print(msg[indx3])
                        
    
    def encrypt(self, msg):
        
        self.spaceInd = find(msg," ")
        
        msg = msg.replace(" ", "")
        self._prepareMsg(msg.lower())
        cipher = ["" for i in range(len(self.preparedMsg))]
        
        self._shiftmatrix()
        print(self.key_matrix)
        
        self._replaceRows(cipher)
        print(cipher)
        self._replaceCols(cipher)
        print(cipher)
        self._replaceBox(cipher)
        print(cipher)
        
        #print(self.preparedMsg)
        #print(cipher)
        print(self.spaceInd)
        #adding back the spaces
        #for indx in range(len(self.spaceInd)):
        #    cipher.insert((self.spaceInd[indx]//2), " ")
        print(cipher)
        return cipher
    
    def decrypt(self, encryptmsg):
        
        self.spaceInd = find(encryptmsg," ")
        encryptmsg = encryptmsg.replace(" ", "")
        self._prepareMsg(encryptmsg.lower())
        plaintext = ["" for i in range(len(self.preparedMsg))]
        print(self.preparedMsg)
        
        self._shiftmatrix()
        
        self._restoreRows(plaintext)
        print(plaintext)
        self._restoreCols(plaintext)
        print(plaintext)
        self._restoreBox(plaintext)
        print(plaintext)
        
        print(self.spaceInd)
        #adding back the spaces
        #for indx in range(len(self.spaceInd)):
        #    plaintext.insert((self.spaceInd[indx]//2), " ")
            
        print(plaintext)
        
        self.preparedMsg.clear()
        
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
        msgHandler = EncryptionSub(key)
        
        if(mode == "E"):
            msg = msgHandler.encrypt(msg)
            
        elif (mode == "D"):
            msg = msgHandler.decrypt(msg)
            
    elif(SubTan == "T"):
        msgHandler = EncryptionTran(key)
        
        if(mode == "E"):
            msg = msgHandler.encrypt(msg)
            
        elif (mode == "D"):
            msg = msgHandler.decrypt(msg)
    

    file_object.seek(0)
    file_object.writelines(msg)
    file_object.truncate()
    file_object.close()
    
    