#!/usr/bin/python3

import random, os, subprocess, tempfile, fuzzingbook, functions
from functions import fuzzer

file = tempfile.mkdtemp()
file = os.path.join(file, 'index.formula')

program = 'bc'
trials = 100
runs = list()


for i in range(trials):
    data = fuzzer()
    with open(file, "w") as f:
        f.write(data)
    result = subprocess.run([program, file],
                            stdin=subprocess.DEVNULL,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    runs.append((data, result))


# let's check the good things first
#print([data for (data, result) in runs if result.stderr == ''])
print(sum([1 for (data, result) in runs if result.stderr == '']))

# let's check the bad outputs then ... 
print([data for (data, result) in runs if result.stderr != ''])