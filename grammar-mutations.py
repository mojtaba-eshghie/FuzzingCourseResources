#!/usr/bin/python3

from fuzzingbook.MutationFuzzer import *
from mutation_functions import *


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



number_of_seeds = 1

seeds = [
    simple_grammar_fuzzer(
        grammar=URL_GRAMMAR,
        max_nonterminals=10) for i in range(number_of_seeds)]

m = MutationFuzzer(seeds)

fuzzed = [m.fuzz() for i in range(0, 10)]
print(fuzzed)




print('###################### section 2 ########################3')

'''
Here, we have a grammar that uses the '<' and '>' symbols themselves the expansion
should contain them, so we have no other way to define an expansion having them except
defining two corresponding terminals for them
'''
simple_nonterminal_grammar = {
    "<start>": ["<nonterminal>"],
    "<nonterminal>": ["<left-angle><identifier><right-angle>"],
    "<left-angle>": ["<"],
    "<right-angle>": [">"],
    "<identifier>": ["id"]  # for now
}

