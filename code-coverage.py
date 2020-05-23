#!/usr/bin/python3

from fuzzingbook.Coverage import Coverage, cgi_decode
from sys import settrace
from functions import fuzzer


def giveMax(a, b, c):
    return max((a, b, c))

def traceit(frame, event, arg):
    print(frame.f_code)
    print(frame.f_lineno)
    print(frame.f_locals)
    print(event)
    print(arg)
    print('======= ======= === ======== ====== === ==== ==== == ======')

'''
with Coverage() as cov:
    #cgi_decode("a+b")
    giveMax(1, 2, 3)
    print(cov.trace())
    print(cov.coverage())
'''

settrace(traceit)

input_string = fuzzer(100)
output_string = cgi_decode(input_string)

settrace(None)