#!/usr/bin/python3

#from fuzzingbook.MutationFuzzer import *
from urllib.parse import urlparse
from fuzzingbook.Fuzzer import fuzzer
import random

def delete_random_character(s):
    if s == "":
        return s
    
    pos = random.randint(0, len(s) - 1)
    return s[:pos] + s[pos + 1:]

def insert_random_character(s):
    """Returns s with a random character inserted"""
    pos = random.randint(0, len(s))
    random_character = chr(random.randrange(32, 127))
    # print("Inserting", repr(random_character), "at", pos)
    return s[:pos] + random_character + s[pos:]

def flip_random_character(s):
    """Returns s with a random bit flipped in a random position"""
    if s == "":
        return s

    pos = random.randint(0, len(s) - 1)
    c = s[pos]
    bit = 1 << random.randint(0, 6)
    new_c = chr(ord(c) ^ bit)
    # print("Flipping", bit, "in", repr(c) + ", giving", repr(new_c))
    return s[:pos] + new_c + s[pos + 1:]


def mutate(s):
    """Return s with a random mutation applied"""
    mutators = [
        delete_random_character,
        insert_random_character,
        flip_random_character
    ]
    mutator = random.choice(mutators)
    # print(mutator)
    return mutator(s)

seed_input = 'A quick brown fox'

'''
for i in range(10):
    x = delete_random_character(seed_input)
    print(repr(x))
'''

for i in range(10):
    print(repr(mutate("A quick brown fox")))