#!/usr/bin/python3

from fuzzingbook.MutationFuzzer import *
from urllib.parse import urlparse
from fuzzingbook.Fuzzer import fuzzer

def http_program(url):
    supported_schemes = ['http', 'https']
    result = urlparse(url)
    if result.scheme not in supported_schemes:
        raise ValueError("Scheme must be one of " + supported_schemes.__str__())
    if result.netloc == '':
        raise ValueError("The host address must not be empty")
    return True


seed_input = 'http://www.google.com/search?q=fuzzing'
mutation_fuzzer = MutationFuzzer(seed=[seed_input])
m_fuz_list = [mutation_fuzzer.fuzz() for i in range(10)]

parse_result = urlparse(seed_input)

# printable assci characters
# print(fuzzer(char_start=32, char_range=96))
trials = 100000

with Timer() as timer:
    for i in range(trials):
        try:
            url = fuzzer(char_start=32, char_range=96)
            http_program(url)
            print("success!  the url string is: \n {}".format(url))
        except ValueError:
            pass

duration_per_run_in_seconds = timer.elapsed_time() / trials

print('--------------------------------')
print(duration_per_run_in_seconds)
