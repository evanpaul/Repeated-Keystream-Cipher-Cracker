# Repeated Keystream Cipher Cracker (RKCC)
The intention of this repository is mostly just to store an online copy. Aside from perhaps educational purposes, there is very little point in cloning or forking it.
## Why?
This code was written as a solution to a project for my Applied Cryptography course. We were given ten ciphertexts in binary and informed that they were produced from English plaintexts XOR'd with a keystream. Each keystream is the repetition of an English word or phrase. None of the plaintexts contain spaces or symbols. The alphabet uses a 5-bit encoding scheme from a(~00000) to z(11001).

 Using this information I implemented a way of conjecturing the length of the key (Kasiski/Babbage Analysis). Once the key length was determined, there were two methods I used for deducing the key:
* XORs of English alphabet against subsets of the ciphertext (A modified version of Kasiski/Babbage's attack)
* Multithreaded dictionary attack (for the stubborn ciphertexts)

## Solutions explained
### Kasiski/Babbage Analysis
[Charles Babbage](https://en.wikipedia.org/wiki/Charles_Babbage) most likely created this method first (to crack the [Vigenère cipher](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher)), but did not immediately publish it. [Friedrich Kasiski](https://en.wikipedia.org/wiki/Friedrich_Kasiski) later independently created and published the method, resulting in him often being credited as the original creator.

This method looks for repeated [digraphs](https://www.math.cornell.edu/~mec/2003-2004/cryptography/subs/digraphs.html) within the ciphertext. This method works best for lengthy ciphertexts and will produce some false-positives. Thus the result set has to be manually observed to find a reasonable key length (which of course may be incorrect).

After a key length is determined, the next step would normally entail splitting the ciphertext into columns based on the key length, and perform a frequency analysis on each column. A key could be deduced once the results are compared to a standard English letter frequency distribution. However, this method degrades as the size of the ciphertext decreases, so I chose a different method.

Instead of running a frequency analysis on each column, I XOR'd each letter of the English alphabet (from most frequently occuring to least) and checked if it ever produces a non-encodable character in a particular column. If it doesn't, that letter is added to a result set. Manual observation of the result set as well as some trial and error leads to the correct key.

### Multi-threaded dictionary attack
This attack is mostly self-explanatory and was used for the smaller ciphertexts. A word list is generated from the chosen dictionary, using the result set from the Kasiski/Babbage Analysis as a filter. RKCC detects the number of available cores on the system and spawns that many threads. Each thread gets a chunk of the word list to try as a key and a blocking call waits for their completion to aggregate and display the results.
## Files
* ciphertexts/ -> Contains all ten ciphertexts
* dictionaries/ -> English word lists
* rkcc.py -> Implementation of analytical methods and attacks
* scheme.py -> 5-bit encoding scheme
* rkcc_tests.py -> Example tests of rkcc methods
* solutions.txt -> Solutions i.e. keys to each ciphertext
* README.md -> You are here
