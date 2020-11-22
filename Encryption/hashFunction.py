import random
from matplotlib import pyplot as plt
import numpy as np


def hashf(word):
    #an Initialization vector for later use.
    IV = 98948498
    
    #if input is a string
    if isinstance(word, str):
        #we convert some of its letters to ints to work on them.
        #because python doesn't allow bitwise operators on strings.
        
        low = ord(word[0]) ^ 8646546
        mid = ~len(word)^ 756576764
        high = ord(word[len(word)-1])^ 8456844654
    else:
        #if it's an integer we'll work on it directly.
        mid = ~word ^ 756756746
        low = word ^ 656965655
        high = ~word ^ 76567527
        
    #taking the lower 4 bits of the word.
    lower = low ^ 65716467
    
    #taking the upper 4 bits of the word.
    upper = high ^ 735957159
    
    #taking the middle bits.
    middle = mid ^ 337677750
    
    #Xor the upper part with the lower part and the middle.
    lower = lower ^ IV
    upper = ~upper ^ lower
    lower = lower & ~middle
    upper = upper & middle
    
    #shifting around the upper and lower
    upper *= upper >> 5
    lower *= lower << 5
    #making sure the return value is in the range [0,256] which is as much as
    #8bits can take. 
    return (upper+lower+~middle) % 256

def generateRandomWord(k):
    #generate random bits of size k
    a = random.getrandbits(k)
    #returns it in string form as python can't really handle bits directly
    #unless we're willing to complicate stuff a bit.
    return str(a)

def generateSqWord(k):
    #generates a sequence of bits where each one returned isn't very different
    #than the input given.
    
    #if it's a string, we'll convert it to int and add 10 to it. otherwise,
    #just add 10 and return.
    if isinstance(k, str):
        k = ord(k)+10
        return k
    else:
        k += 10
        return k

#start of main
if(__name__ == "__main__"):
    
    #creating the buckets as 2D lists.
    buckets = [[] for i in range(256)]
    
    #creating the x_axis for the plot.
    x_axis = np.arange(256)
    
    #variables to be used in the loops.
    y_axis = []
    chisquare = 0
    word = "h"
    
    for i in range(2000):
        #generating 2000 random words between 10 and 80000.
        word = generateRandomWord(random.randint(10,80000))
        #adding the digests into their bucket using the hash function.
        buckets[hashf(word)].append(hash(word))
        
        #uncomment this to try the inputs with minimal change test (comment the first word).
        #word = generateSqWord(word)
    
    
    for k in range(256):
        #adding the size of each buck to the y axis.
        y_axis.append(len(buckets[k]))
        #calculating the chisquare.
        chisquare += ( len(buckets[k])*len(buckets[k])+ 1) /2
    
    #finishing the calculation for the chisquare.
    denom = (2000/(2*256)) * (2000+(2*256)-1)
    chisquare = chisquare / denom
    print(str(chisquare))
    
    #building the plot.
    plt.bar(x_axis, y_axis)
    
    plt.title("Hash function distribution")
    plt.xlabel("Buckets")
    plt.ylabel("collision/occurrences")
    plt.show()