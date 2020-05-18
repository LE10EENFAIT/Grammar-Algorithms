# Grammar Algorithms
Algorithms for grammar analysis for  Python 3 with nltk

# Requirements
- [nltk](https://www.nltk.org/)

Run `pip3 install -r requirements.txt`

# Usage
Run `python3 grammar_algos.py -f [path of the file containing the grammar]` and follow instructions on the terminal

# Algorithms implemented
- [CYK algorithm](https://en.wikipedia.org/wiki/CYK_algorithm)

- [First algorithm (for an LL parser)](https://en.wikipedia.org/wiki/LL_parser)

# Template of grammar
### 1.

E -> T EP  
EP -> '+' T EP | 'ε'  
T -> F TP  
TP -> '*' F TP | 'ε'  
F -> '(' E ')' | 'id'  

#### Output for first algorithm:
```
The first table for this grammar is:
First(E) = {'(', 'id'}
First(EP) = {'+', 'ε'}
First(T) = {'(', 'id'}
First(TP) = {'*', 'ε'}
First(F) = {'(', 'id'}
```

### 2.

S -> NP VP  
PP -> P NP  
NP -> Det N | NP PP  
VP -> V NP | VP PP  
Det -> 'the'  
N -> 'kids' | 'box' | 'floor'  
V -> 'opened'  
P -> 'on'  

#### Output for CYK algorithm with the word "the kids opened the box on the floor":
```
CYK algorithm for the kids opened the box on the floor :

[[Det], [NP], 'ø', 'ø', [S], 'ø', 'ø', [S]]
['ø', [N], 'ø', 'ø', 'ø', 'ø', 'ø', 'ø']
['ø', 'ø', [V], 'ø', [VP], 'ø', 'ø', [VP]]
['ø', 'ø', 'ø', [Det], [NP], 'ø', 'ø', [NP]]
['ø', 'ø', 'ø', 'ø', [N], 'ø', 'ø', 'ø']
['ø', 'ø', 'ø', 'ø', 'ø', [P], 'ø', [PP]]
['ø', 'ø', 'ø', 'ø', 'ø', 'ø', [Det], [NP]]
['ø', 'ø', 'ø', 'ø', 'ø', 'ø', 'ø', [N]]
the kids opened the box on the floor is in the grammar
```
