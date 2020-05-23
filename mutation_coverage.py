#!/usr/bin/python3

from fuzzingbook.MutationFuzzer import *
from fuzzingbook.Fuzzer import *



seed_input = "http://www.google.com/search?q=fuzzing"

mutation_fuzzer = MutationCoverageFuzzer(seed=[seed_input])
mutation_fuzzer.runs(http_runner, trials=10000)
print(mutation_fuzzer.population[:5])


