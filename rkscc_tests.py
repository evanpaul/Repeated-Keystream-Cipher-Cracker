#!/usr/bin/env python
# Repeated Key Stream Cipher Cracker tests
from rkscc import *
prefix = "ciphertexts/"

# Examples
C17 = parse(prefix+"C17.txt")
analyze(C17) # Analysis shows likely key lengths are: 8 and 16
threaded_dictionary_attack(C17, 8) # key = 'exclaims'

C60 = parse(prefix+"C60.txt")
analyze(C60) # Analysis once again shows likely key lengths are: 8 and 16
threaded_dictionary_attack(C60, 8, phrase_flag=False) # Too many choices => turn off phrase_Flag; key = 'supports'
