#!/usr/bin/python3

import re, random


# to use the railroad diagram variation:
from RailRoadDiagrams import NonTerminal, Terminal, Choice, HorizontalChoice, Sequence, Diagram, show_diagram
from IPython.display import SVG, display
from itertools import zip_longest
import datetime



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


def syntax_diagram_symbol(symbol):
    if is_nonterminal(symbol):
        return NonTerminal(symbol[1:-1])
    else:
        return Terminal(symbol)

def syntax_diagram_expr(expansion):
    # In later chapters, we allow expansions to be tuples,
    # with the expansion being the first element
    if isinstance(expansion, tuple):
        expansion = expansion[0]

    symbols = [sym for sym in re.split(RE_NONTERMINAL, expansion) if sym != ""]
    
    if len(symbols) == 0:
        symbols = [""]  # special case: empty expansion

    return Sequence(*[syntax_diagram_symbol(sym) for sym in symbols])
 

def syntax_diagram_alt(alt):
    max_len = 5
    alt_len = len(alt)
    if alt_len > max_len:
        iter_len = alt_len // max_len
        alts = list(zip_longest(*[alt[i::iter_len] for i in range(iter_len)]))
        exprs = [[syntax_diagram_expr(expr) for expr in alt
                  if expr is not None] for alt in alts]
        choices = [Choice(len(expr) // 2, *expr) for expr in exprs]
        return HorizontalChoice(*choices)
    else:
        return Choice(alt_len // 2, *[syntax_diagram_expr(expr) for expr in alt])


def syntax_diagram(grammar):
    from IPython.display import SVG, display

    for key in grammar:
        print("%s" % key[1:-1])
        #display(SVG(show_diagram(syntax_diagram_alt(grammar[key]))))

        svg_display_obj = SVG(show_diagram(syntax_diagram_alt(grammar[key])))
        
        

        now = datetime.datetime.now()
        filename = now.strftime("%Y-%m-%d-%H-%M-%S" + key + ".svg")
        with open('svg/' + filename, 'w') as svg_file:
            svg_file.write(svg_display_obj.data)

#svg_display_obj = SVG(show_diagram(syntax_diagram_symbol('<term>')))
#svg_display_obj = SVG(show_diagram(syntax_diagram_expr(grammar['<start>'][0])))
'''
svg_display_obj = SVG(show_diagram(syntax_diagram_alt(grammar['<digit>'])))

now = datetime.datetime.now()
filename = now.strftime("%Y-%m-%d-%H-%M-%S.svg")
with open('svg/' + filename, 'w') as svg_file:
    svg_file.write(svg_display_obj.data)

'''


syntax_diagram(grammar)