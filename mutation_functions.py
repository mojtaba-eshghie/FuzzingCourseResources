#!/usr/bin/python3

import re, random


# to use the railroad diagram variation:
from RailRoadDiagrams import NonTerminal, Terminal, Choice, HorizontalChoice, Sequence, Diagram, show_diagram
from IPython.display import SVG, display
from itertools import zip_longest




RE_NONTERMINAL = re.compile(r'(<[^<> ]*>)')
START_SYMBOL = '<start>'


grammar = {
    '<start>': ['<phone-number>'],
    '<phone-number>': ['(<country-code>)<operator-code><triplex><four-digits>'],
    '<country-code>': ['0098'],
    '<operator-code>': ['911', '935', '921'], # We assume three country codes for IR-MCI, Rittel, and Irancell
    '<triplex>': ['<digit><digit><digit>'],
    '<four-digits>': ['<digit><digit><digit>'],
    '<digit>': [str(i) for i in range(10)]
}



URL_GRAMMAR = {
    "<start>":
        ["<url>"],
    "<url>":
        ["<scheme>://<authority><path><query>"],
    "<scheme>":
        ["http", "https", "ftp", "ftps"],
    "<authority>":
        ["<host>", "<host>:<port>", "<userinfo>@<host>", "<userinfo>@<host>:<port>"],
    "<host>":  # Just a few
        ["cispa.saarland", "www.google.com", "fuzzingbook.com"],
    "<port>":
        ["80", "8080", "<nat>"],
    "<nat>":
        ["<digit>", "<digit><digit>"],
    "<digit>":
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
    "<userinfo>":  # Just one
        ["user:password"],
    "<path>":  # Just a few
        ["", "/", "/<id>"],
    "<id>":  # Just a few
        ["abc", "def", "x<digit><digit>"],
    "<query>":
        ["", "?<params>"],
    "<params>":
        ["<param>", "<param>&<params>"],
    "<param>":  # Just a few
        ["<id>=<id>", "<id>=<nat>"],
}


def nonterminals(expansion):
    """
    Returns the nonterminals (the strings matching the following
    re pattern):
    (<[^<>]*>)
    """
    if isinstance(expansion, tuple):
        expansion = expansion[0]
    return re.findall(RE_NONTERMINAL, expansion)

def is_nonterminal(expansion):
    return re.match(RE_NONTERMINAL, expansion)

class ExpansionError(Exception):
    pass

def simple_grammar_fuzzer(grammar, start_symbol=START_SYMBOL,
                          max_nonterminals=10, max_expansion_trials=100,
                          log=False):
    term = start_symbol
    expansion_trials = 0

    while len(nonterminals(term)) > 0:
        symbol_to_expand = random.choice(nonterminals(term))
        expansions = grammar[symbol_to_expand]
        expansion = random.choice(expansions)
        new_term = term.replace(symbol_to_expand, expansion, 1)
        

        if len(nonterminals(new_term)) < max_nonterminals:
            term = new_term
            if log:
                print("%-40s" % (symbol_to_expand + " -> " + expansion), term)
            expansion_trials = 0
        else:
            expansion_trials += 1
            if expansion_trials >= max_expansion_trials:
                raise ExpansionError("Cannot expand " + repr(term))

    return term

