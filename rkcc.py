#!/usr/bin/env python
### Repeated Key Stream Cipher Cracker implementation ###
import scheme
import numpy as np
import sys
import pprint
import timeit
from multiprocessing import Process, Queue, cpu_count
# Globals
NUM_CORES = cpu_count() # For dictionary attack
pp = pprint.PrettyPrinter(indent=4)

# Analyze a ciphertext and list any repeated digraphs in order to divine the key length
def analyze(ciphertext):
    i = 0
    character_map = {}
    print len(ciphertext), "characters"
    # Map all of the ciphertext character blocks
    while i < len(ciphertext):
        chunk = ciphertext[i:(i+5)]
        block = scheme.dec(chunk)
        # If the key isn't already there
        if not character_map.has_key(block):
            if block == '?':
                character_map[block] = [chunk, i/5]
            else:
                character_map[block] = [i/5]
        # If the key is already there
        else:
            if block == '?':
                character_map[block].append([chunk, i/5])
            else:
                character_map[block].append(i/5)

        i+=5
    print i/5, "blocks"

    # Form an adjacency list i.e. a list of digraphs
    adj_map = {}
    character_map.pop("?", None) # Unless we're desperately in need of more data, this case isn't worth the headache of handling
    q = character_map.items()
    for i in range(len(q)):
        current = q[i][0] # Current letter we're looking at
        locations = q[i][1] # In which chunk it occurs
        for j in range(len(locations)):
            ltr_pos = (locations[j] + 1)*5 # Bit position of adjacent characters
            ltr = scheme.dec(ciphertext[ltr_pos:(ltr_pos+5)]) # Adjacent character
            # Log all digraphs
            # New entry
            if not adj_map.has_key(current):
                adj_map[current] = {ltr: [ltr_pos/5]}
            else:
                # Check for adjacent existance
                if adj_map[current].has_key(ltr):
                    adj_map[current][ltr].append(ltr_pos/5)
                else:
                    adj_map[current][ltr] = [ltr_pos/5]
    # Narrow down adjacency map by removing useless (size=1) entries i.e. nonrepeated digraphs
    for k in adj_map.keys():
        for l in adj_map[k].keys():
            if len(adj_map[k][l]) == 1:
                del adj_map[k][l]
        if not adj_map[k]:
            del adj_map[k]
    # Now that the list is narrowed: calculate distances between repeated digraphs
    # result[digraph] = ([digraph distances], gcd of distances)
    # From observation we can most likely guess a keylength
    result = {}
    # ASCII encodings: 97 => a, 122 => z
    for m in range(97, 123):
        if adj_map.has_key(chr(m)):
            for n in range(97, 123):
                if adj_map[chr(m)].has_key(chr(n)):
                    diff_list = []
                    for o in range(len(adj_map[chr(m)][chr(n)])-1):
                        # Distance calculations
                        diff = adj_map[chr(m)][chr(n)][o+1] - adj_map[chr(m)][chr(n)][o]
                        diff_list.append(diff)
                    g = GCDs(diff_list)
                    digraph = ""+chr(m)+chr(n) # Make a key from digraph
                    result[digraph] = (diff_list, g)
    print "Digraph distances:"
    pp.pprint(result)
# Method 1: XOR with characters (preferably most occuring to least occuring) based on subsets with size of guessed keylength
def fold_and_xor(text, keylength, column):
    # Different sources give different sortings, but it's not incredibly pertinent to be correct here
    # Sorting is from most frequntly occurring to least frequently occurring.
    # This doesn't increase performance, but it makes conjecturing keys easier
    sorted_letters = ['e','t','a','o','i','n','s','h','r','d','l','u','c','m','w','f','g','y','p','b','v','k','j','x','q','z']
    i = 0
    j = 0
    key_bits = keylength * 5

    # "Fold" ciphertext into rows of length=key_bits.
    # XOR letters into each column and see if that letter works for each chunk
    # If it does, it is a possibility that needs to be considered
    possibilities = []
    for l in sorted_letters:
        encoding_flag = True
        i = 5*(column-1)
        while i < len(text):
            # If encoding scheme doesn't work, either keylength is wrong or current character is wrong
            if scheme.dec(scheme.XOR(text[i:(i+5)], scheme.enc(l))) == '?':
                encoding_flag = False
                break
            i+=(5*keylength) # Jump to next row
        if encoding_flag:
            possibilities.append(l)
    # Column number corresponds to letter #
    return possibilities
# Print one chunk per line
def print_chunks(arr):
    i = 0
    while i < len(arr):
        print arr[i:(i+5)], scheme.scheme.dec(arr[i:(i+5)]), i/5
        i+=5
# Parse bitstream from file into numpy array
def parse(file_name):
    l = []
    with open(file_name) as f:
      while True:
        c = f.read(1).strip()
        if not c:
            break
        if c:
            l.append(int(c))

    # Formatting
    bits = len(l)
    a = file_name + "   ("+str(bits)+" bits, "+str(bits/5)+" characters)"
    b = len(a)
    print '='*b
    print a
    print "="*b

    return np.array(l, dtype=int)
# Decrypt stream cipher with repeated keystream
def decrypt(text, keyword):
    key = scheme.encode(keyword)
    keylen = len(key)
    i = 0
    key_str = "\nKEY = "+keyword.upper()+":\n"
    result = [key_str]

    while i < len(text):
        key_chunk = mod_arr(key, i%keylen, (i+5)%keylen)
        result.append(scheme.dec(scheme.XOR(text[i:(i+5)], key_chunk))),
        i += 5
    return "".join(result)
# Modularize an array e.g. if array = [2,4,6,8], then mod_arr(array, 3, 2) = [6, 8, 2]
def mod_arr(arr, start, stop):
    out = []
    if start < stop:
        return arr[start:stop]
    i = start
    while i != stop:
        out.append(arr[i%len(arr)])
        i = (i+1)%len(arr)
    return out
def GCD(a, b):
    if b == 0:
        return a
    else:
        return GCD(b, a%b)
# type(in_set) => tuple/list
def GCDs(in_set):
    return reduce(GCD, in_set)
# Multi-threaded sub-routine for optimized attack
def dictionary_attack(thread_num, result_queue, key_list, text):
    result = []
    subset = len(key_list)/NUM_CORES # Divide key list into sections based on number of cores
    # Try section of key list corresponding t
    for key in key_list[((thread_num-1)*subset):(thread_num*subset)]:
        if key:
            result.append(decrypt(text, key))

    result_queue.put(result)
    return
# Run analyze() first to guess likely lengths
def threaded_dictionary_attack(ciphertext, length, phrase_flag = True):
    print "Detected",NUM_CORES,"CPUs"
    print "Running threaded dictionary attack with length =",length
    start = timeit.default_timer() # Begin timer
    # Column analysis, get possible letters for each column/slot
    letters = []
    for i in range(1,length+1):
        letters.append(fold_and_xor(ciphertext, length, i))

    ############### DICTIONARIES ################
    # dictionaries/words1.txt ~10K  (awful)     #
    # dictionaries/words2.txt ~240k (decent)    #
    # dictionaries/words3.txt ~350k (excellent) #
    #############################################
    keys = []
    words = 0
    total = 0
    with open("dictionaries/words3.txt") as f:
        for line in f:
            total +=1
            target = line.strip()
            match_flag = True
            # Check word against possible permutations
            if (phrase_flag and len(target) != 1) or len(target) == length:
                smaller = min(len(target), length)
                for j in range(smaller):
                    if target[j] not in letters[j]:
                        match_flag = False
                if match_flag:
                    keys.append(target)
                    words+=1
    print "Loaded",words,"/",total,"words"

    # Multi-threading for parallel processing
    q = Queue()
    threads = []
    results = [None]*NUM_CORES
    # Instantiate and start threads
    for i in range(1, NUM_CORES+1):
        t = Process(target=dictionary_attack, args=(i, q, keys, ciphertext))
        threads.append(t)
        t.start()
        results[(i-1)] = q.get()
    # Blocking call to resolve threads
    for thread in threads:
        thread.join()
    # Display results
    tries = 0
    for thread_results in results:
        for pt in thread_results:
            tries +=1
            print pt
    # End timer
    end = timeit.default_timer()
    elapsed = end-start

    print "Runtime:",elapsed,"seconds"
    print tries,"attempts"
    return elapsed
