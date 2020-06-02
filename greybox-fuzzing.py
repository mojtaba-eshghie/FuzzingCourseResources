#!/usr/bin/python3

import random
from fuzzingbook.Coverage import Coverage, population_coverage

trials = 10

class Mutator(object):
    def __init__(self):
        self.mutators = [
            self.delete_random_character,
            self.insert_random_character,
            self.flip_random_character
        ]

    def insert_random_character(self,s):
        """Returns s with a random character inserted"""
        pos = random.randint(0, len(s))
        random_character = chr(random.randrange(32, 127))
        return s[:pos] + random_character + s[pos:]
    
    def delete_random_character(self,s):
        """Returns s with a random character deleted"""
        if s == "":
            return self.insert_random_character(s)

        pos = random.randint(0, len(s) - 1)
        return s[:pos] + s[pos + 1:]
    
    def flip_random_character(self,s):
        """Returns s with a random bit flipped in a random position"""
        if s == "":
            return self.insert_random_character(s)

        pos = random.randint(0, len(s) - 1)
        c = s[pos]
        bit = 1 << random.randint(0, 6)
        new_c = chr(ord(c) ^ bit)
        return s[:pos] + new_c + s[pos + 1:]
    
    def mutate(self, inp):
        """Return s with a random mutation applied"""
        mutator = random.choice(self.mutators)
        return mutator(inp)
    

myMutator = Mutator()
seed = 'Good Morning!'
mutated_list = []

for trial in range(trials):
    mutated_list.append(myMutator.mutate(seed))

print(mutated_list)