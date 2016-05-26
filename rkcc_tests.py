#!/usr/bin/env python
# Repeated Key Stream Cipher Cracker tests
from rkcc import *
p = "ciphertexts/"

## EXAMPLES ##
# Example 1: Lengthy ciphertext
C17 = parse(p+"C17.txt") # key = 'exclaims'
analyze(C17) # Analysis shows likely key lengths are: 8 and 16
key_length = 8
for i in range(1, key_length+1): # fold_and_xor currently only works on one column at a time
    print fold_and_xor(C17, key_length, i)
# Example 2: Short ciphertext
C60 = parse(p+"C60.txt")
analyze(C60) # Analysis once again shows likely key lengths are: 8 and 16
threaded_dictionary_attack(C60, 8, phrase_flag=False) # Too many choices => turn off phrase_Flag; key = 'supports'
