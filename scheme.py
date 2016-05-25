#!/usr/bin/env python
# Encoding Scheme
# Decode a chunk (5 bits)
import numpy as np

def dec(ct):
    if np.array_equal(np.array([0, 0, 0, 0, 0], dtype=int), ct):
        return 'a'
    elif np.array_equal(np.array([0, 0, 0, 0, 1], dtype=int), ct):
        return 'b'
    elif np.array_equal(np.array([0, 0, 0, 1, 0], dtype=int), ct):
        return 'c'
    elif np.array_equal(np.array([0, 0, 0, 1, 1], dtype=int), ct):
        return 'd'
    elif np.array_equal(np.array([0, 0, 1, 0, 0], dtype=int), ct):
        return 'e'
    elif np.array_equal(np.array([0, 0, 1, 0, 1], dtype=int), ct):
        return 'f'
    elif np.array_equal(np.array([0, 0, 1, 1, 0], dtype=int), ct):
        return 'g'
    elif np.array_equal(np.array([0, 0, 1, 1, 1], dtype=int), ct):
        return 'h'
    elif np.array_equal(np.array([0, 1, 0, 0, 0], dtype=int), ct):
        return 'i'
    elif np.array_equal(np.array([0, 1, 0, 0, 1], dtype=int), ct):
        return 'j'
    elif np.array_equal(np.array([0, 1, 0, 1, 0], dtype=int), ct):
        return 'k'
    elif np.array_equal(np.array([0, 1, 0, 1, 1], dtype=int), ct):
        return 'l'
    elif np.array_equal(np.array([0, 1, 1, 0, 0], dtype=int), ct):
        return 'm'
    elif np.array_equal(np.array([0, 1, 1, 0, 1], dtype=int), ct):
        return 'n'
    elif np.array_equal(np.array([0, 1, 1, 1, 0], dtype=int), ct):
        return 'o'
    elif np.array_equal(np.array([0, 1, 1, 1, 1], dtype=int), ct):
        return 'p'
    elif np.array_equal(np.array([1, 0, 0, 0, 0], dtype=int), ct):
        return 'q'
    elif np.array_equal(np.array([1, 0, 0, 0, 1], dtype=int), ct):
        return 'r'
    elif np.array_equal(np.array([1, 0, 0, 1, 0], dtype=int), ct):
        return 's'
    elif np.array_equal(np.array([1, 0, 0, 1, 1], dtype=int), ct):
        return 't'
    elif np.array_equal(np.array([1, 0, 1, 0, 0], dtype=int), ct):
        return 'u'
    elif np.array_equal(np.array([1, 0, 1, 0, 1], dtype=int), ct):
        return 'v'
    elif np.array_equal(np.array([1, 0, 1, 1, 0], dtype=int), ct):
        return 'w'
    elif np.array_equal(np.array([1, 0, 1, 1, 1], dtype=int), ct):
        return 'x'
    elif np.array_equal(np.array([1, 1, 0, 0, 0], dtype=int), ct):
        return 'y'
    elif np.array_equal(np.array([1, 1, 0, 0, 1], dtype=int), ct):
        return 'z'
    else:
        return '?'
# Decode multiple chunks
def decode(ct):
    output = ""
    for i in range(ct.size/5):
        output += dec(ct[(0+5*i):(5+5*i)])
    return output
# Encode a chunk
def enc(ct):
    if ct == 'a':
        return np.array([0, 0, 0 ,0, 0], dtype=int)
    elif ct == 'b':
        return np.array([0, 0, 0 ,0, 1], dtype=int)
    elif ct == 'c':
        return np.array([0, 0, 0 ,1, 0], dtype=int)
    elif ct == 'd':
        return np.array([0, 0, 0 ,1, 1], dtype=int)
    elif ct == 'e':
        return np.array([0, 0, 1 ,0, 0], dtype=int)
    elif ct == 'f':
        return np.array([0, 0, 1 ,0, 1], dtype=int)
    elif ct == 'g':
        return np.array([0, 0, 1 ,1, 0], dtype=int)
    elif ct == 'h':
        return np.array([0, 0, 1 ,1, 1], dtype=int)
    elif ct == 'i':
        return np.array([0, 1, 0 ,0, 0], dtype=int)
    elif ct == 'j':
        return np.array([0, 1, 0 ,0, 1], dtype=int)
    elif ct == 'k':
        return np.array([0, 1, 0 ,1, 0], dtype=int)
    elif ct == 'l':
        return np.array([0, 1, 0 ,1, 1], dtype=int)
    elif ct == 'm':
        return np.array([0, 1, 1 ,0, 0], dtype=int)
    elif ct == 'n':
        return np.array([0, 1, 1 ,0, 1], dtype=int)
    elif ct == 'o':
        return np.array([0, 1, 1 ,1, 0], dtype=int)
    elif ct == 'p':
        return np.array([0, 1, 1 ,1, 1], dtype=int)
    elif ct == 'q':
        return np.array([1, 0, 0 ,0, 0], dtype=int)
    elif ct == 'r':
        return np.array([1, 0, 0 ,0, 1], dtype=int)
    elif ct == 's':
        return np.array([1, 0, 0 ,1, 0], dtype=int)
    elif ct == 't':
        return np.array([1, 0, 0 ,1, 1], dtype=int)
    elif ct == 'u':
        return np.array([1, 0, 1 ,0, 0], dtype=int)
    elif ct == 'v':
        return np.array([1, 0, 1 ,0, 1], dtype=int)
    elif ct == 'w':
        return np.array([1, 0, 1 ,1, 0], dtype=int)
    elif ct == 'x':
        return np.array([1, 0, 1 ,1, 1], dtype=int)
    elif ct == 'y':
        return np.array([1, 1, 0 ,0, 0], dtype=int)
    elif ct == 'z':
        return np.array([1, 1, 0 ,0, 1], dtype=int)
    else:
        print 'ENCODING UNKNOWN:', ct
# Encode multiple chunks
def encode(ct):
    s = np.array([], dtype=int)
    for i in range(len(ct)):
        a = enc(ct[i])
        s = np.concatenate((s, a))
    return s
# XOR two equal length chunks
def XOR(a, b):
    out = np.zeros(len(a), dtype = int)
    if len(a) == len(b):
        for i in range(len(a)):
            out[i] = np.bitwise_xor(a[i], b[i])
    return out
