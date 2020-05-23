#!/usr/bin/python3

import re, random



grammar = {
    '<start>': ['<phone-number>'],
    '<phone-number>': ['(<country-code>)<operator-code><triplex><four-digits>'],
    '<country-code>': ['0098'],
    '<operator-code>': ['911', '935', '921'], # We assume three country codes for IR-MCI, Rittel, and Irancell
    '<triplex>': ['<digit><digit><digit>'],
    '<four-digits>': ['<digit><digit><digit>'],
    '<digit>': [str(i) for i in range(10)]
}
START_SYMBOL = '<start>'

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


RE_NONTERMINAL = re.compile(r'(<[^<> ]*>)')


# just a few verifications of the the pattern 
assert is_nonterminal("<abc>")
assert is_nonterminal("<symbol-1>")
assert not is_nonterminal("+")
assert nonterminals("<term> * <factor>") == ["<term>", "<factor>"]
assert nonterminals("<digit><integer>") == ["<digit>", "<integer>"]
assert nonterminals("1 < 3 > 2") == []
assert nonterminals("1 <3> 2") == ["<3>"]
assert nonterminals("1 + 2") == []
assert nonterminals(("<1>", {'option': 'value'})) == ["<1>"]


print(simple_grammar_fuzzer(grammar, START_SYMBOL, max_nonterminals=10, max_expansion_trials=100, log=True))

for i in range(10):
    print(simple_grammar_fuzzer(grammar=grammar, max_nonterminals=5))