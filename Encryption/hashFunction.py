import string
import sys
import random
from matplotlib import pyplot as plt
import numpy as np


def hash(word):
    IV = 98948498
    if isinstance(word, str):
        low = ord(word[0]) ^ 8646546
        mid = ~len(word)^ 756576764
        high = ord(word[len(word)-1])^ 8456844654
    else:
        mid = ~word ^ 756756746
        low = word ^ 656965655
        high = ~word ^ 76567527
    #taking the lower 4 bits of the word.
    lower = int(low) ^ 65716467
    
    #taking the upper 4 bits of the word.
    upper = int(high) ^ 735957159
    
    middle = mid ^ 337677750
    
    #Xor the upper part with the lower part
    lower = lower ^ IV
    upper = ~upper ^ lower
    lower = lower & ~middle
    upper = upper & middle
    
    upper *= upper >> 5
    lower *= lower << 5
    
    return (int(upper)+int(lower)+int(~middle)) % 256

def generateRandomWord(k):
    a = random.getrandbits(k)
    
    return str(a)

def generateSqWord(k):
    
    if isinstance(k, str):
        k = ord(k)+10
        return k
    else:
        k += 10
        return k


if(__name__ == "__main__"):
    #word = 95989
    
    buckets = [[] for i in range(256)]
    
    
    x_axis = np.arange(256)
    
    y_axis = []
    chisquare = 0
    word = "h"
    for i in range(2000):
        word = generateRandomWord(random.randint(10,80000))
        buckets[hash(word)].append(hash(word))
        #word = generateSqWord(word)
    
    for k in range(256):
        y_axis.append(len(buckets[k]))
        chisquare += ( len(buckets[k])*len(buckets[k])+ 1) /2
        
    denom = (2000/(2*256)) * (2000+(2*256)-1)
    chisquare = chisquare / denom
    plt.bar(x_axis, y_axis)
    print(str(chisquare))
    plt.show()
    #print("word is " + str(word) + " the hash is " + str(hashword) + " and it has size of " + str(sys.getsizeof(hashword)))