# Formal Language Algorithms
Algorithms for formal language written with Python 3 with nltk

# Requirements
- [nltk](https://www.nltk.org/)

Run `pip3 install -r requirements.txt`

# Usage
Run `python3 grammar_algos.py -f [path of the file containing the grammar]` and follow instructions on the terminal

# Algorithms implemented
- [CYK algorithm](https://en.wikipedia.org/wiki/CYK_algorithm)

- [First algorithm (for an LL parser)](https://en.wikipedia.org/wiki/LL_parser)

- [Follow algorithm (for an LL parser)](https://en.wikipedia.org/wiki/LL_parser)

- [LL parser](https://en.wikipedia.org/wiki/LL_parser)

# Template of grammar
### 1.

E -> T EP  
EP -> '+' T EP | 'ε'  
T -> F TP  
TP -> '*' F TP | 'ε'  
F -> '(' E ')' | 'id'  

#### Output for First algorithm:
```
The First sets for this grammar are: 
First(E) = {(, id}
First(EP) = {ε, +}
First(T) = {(, id}
First(TP) = {ε, *}
First(F) = {(, id}
```

#### Output for Follow algorithm:
```
The Follow sets for this grammar are: 
Follow(E) = {$, )}
Follow(EP) = {$, )}
Follow(T) = {$, ), +}
Follow(TP) = {$, ), +}
Follow(F) = {$, ), *, +}
```

#### Output for LL parser (need to be revised):
```
The LL table for this grammar is: 
LL(E, '$') = {}   LL(E, '+') = {}   LL(E, '*') = {}   LL(E, '(') = {E -> T EP}   LL(E, ')') = {}   LL(E, 'id') = {E -> T EP}   
LL(EP, '$') = {EP -> 'ε'}   LL(EP, '+') = {EP -> '+' T EP}   LL(EP, '*') = {}   LL(EP, '(') = {}   LL(EP, ')') = {EP -> 'ε'}   LL(EP, 'id') = {}   
LL(T, '$') = {}   LL(T, '+') = {}   LL(T, '*') = {}   LL(T, '(') = {T -> F TP}   LL(T, ')') = {}   LL(T, 'id') = {T -> F TP}   
LL(TP, '$') = {TP -> 'ε'}   LL(TP, '+') = {TP -> 'ε'}   LL(TP, '*') = {TP -> '*' F TP}   LL(TP, '(') = {}   LL(TP, ')') = {TP -> 'ε'}   LL(TP, 'id') = {}   
LL(F, '$') = {}   LL(F, '+') = {}   LL(F, '*') = {}   LL(F, '(') = {F -> '(' E ')'}   LL(F, ')') = {}   LL(F, 'id') = {F -> 'id'} 
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
CYK algorithm for 'the kids opened the box on the floor' :

[[Det], [NP], 'ø', 'ø', [S], 'ø', 'ø', [S]]
['ø', [N], 'ø', 'ø', 'ø', 'ø', 'ø', 'ø']
['ø', 'ø', [V], 'ø', [VP], 'ø', 'ø', [VP]]
['ø', 'ø', 'ø', [Det], [NP], 'ø', 'ø', [NP]]
['ø', 'ø', 'ø', 'ø', [N], 'ø', 'ø', 'ø']
['ø', 'ø', 'ø', 'ø', 'ø', [P], 'ø', [PP]]
['ø', 'ø', 'ø', 'ø', 'ø', 'ø', [Det], [NP]]
['ø', 'ø', 'ø', 'ø', 'ø', 'ø', 'ø', [N]]
'the kids opened the box on the floor' is in the grammar
```
