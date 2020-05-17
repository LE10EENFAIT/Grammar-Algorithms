# Grammar Algorithms
Algorithms for grammar analysis in Python

# Requirements
[-nltk](https://www.nltk.org/)

Run `pip3 install -r requirements.txt`

# Usage
Run `python3 grammar_algos.py -f [path of the file containing the grammar]` and follow instructions on the terminal

# Algorithms implemented
-[CYK algorithm](https://en.wikipedia.org/wiki/CYK_algorithm)

-[First algorithm (for an LL parser)](https://en.wikipedia.org/wiki/LL_parser)

# Template of grammar
E -> T EP

EP -> '+' T EP | 'ε'

T -> F TP

TP -> '*' F TP | 'ε'

F -> '(' E ')' | 'id'





S -> NP VP

PP -> P NP

NP -> Det N | NP PP

VP -> V NP | VP PP

Det -> 'the'

N -> 'kids' | 'box' | 'floor'

V -> 'opened'

P -> 'on'
