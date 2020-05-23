#!/usr/bin/python3

from fuzzingbook.Fuzzer import Fuzzer
from fuzzingbook.Grammars import *

# 09357705065

IR_PHONE_NUMBER = {
    '<start>': ['<phone-number>'],
    '<phone-number>': ['(<country-code>)<operator-code><triplex><four-digits>'],
    '<country-code>': ['0098'],
    '<operator-code>': ['911', '935', '921'], # We assume three country codes for IR-MCI, Rittel, and Irancell
    '<triplex>': ['<digit><digit><digit>'],
    '<four-digits>': ['<digit><digit><digit>'],
    '<digit>': [str(i) for i in range(10)]
}

assert is_valid_grammar(IR_PHONE_NUMBER)

print([simple_grammar_fuzzer(IR_PHONE_NUMBER) for i in range(5)])