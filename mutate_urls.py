#!/usr/bin/python3

#from fuzzingbook.MutationFuzzer import *
from urllib.parse import urlparse
from fuzzingbook.Fuzzer import fuzzer
import random
from fuzzingbook.Fuzzer import Fuzzer

def http_program(url):
    supported_schemes = ['http', 'https']
    result = urlparse(url)
    if result.scheme not in supported_schemes:
        raise ValueError("Scheme must be one of " + supported_schemes.__str__())
    if result.netloc == '':
        raise ValueError("The host address must not be empty")
    return True

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

def is_valid_url(url):
    try:
        result = http_program(url)
        return True
    except ValueError:
        return False


'''
What if we get to check if the bad cases are not OK? For instance, the following
assersion does exactly this:
'''
assert is_valid_url("http://www.google.com/search?q=fuzzing")
assert not is_valid_url("xyzzy")

seed_input = "http://www.google.com/search?q=fuzzing"
valid_inputs = set()
trials = 200

for i in range(trials):
    inp = mutate(seed_input)
    if is_valid_url(inp):
        valid_inputs.add(inp)


class MutationFuzzer(Fuzzer):
    def __init__(self, seed, min_mutations=2, max_mutations=10):
        self.seed = seed
        self.min_mutations = min_mutations
        self.max_mutations = max_mutations
        self.reset()

    def reset(self):
        self.population = self.seed
        self.seed_index = 0

class MutationFuzzer(MutationFuzzer):
    def mutate(self, inp):
        return mutate(inp)

class MutationFuzzer(MutationFuzzer):
    def create_mutations(self):
        candidate = random.choice(self.population)
        trials = random.randint(self.min_mutations, self.max_mutations)

        for i in range(trials):
            candidate = self.mutate(candidate)
        return candidate