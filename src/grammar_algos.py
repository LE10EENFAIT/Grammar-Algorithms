import nltk
import argparse

eps = 'ε'

def load_grammar(filename):
    f = open(filename, 'r')
    return nltk.CFG.fromstring(f.read())

##Implementation of CYK algorithm
def CYK(grammar, word, solve=True):

    def trace_cyk(cyk):
        for i in range(len(cyk)):
            print(cyk[i])

    ##Init
    size_word = len(word)
    cyk = [['ø' for i in range(size_word)] for j in range(size_word)]

    for i in range(size_word):
        prod = grammar.productions(rhs=word[i])
        cyk[i][i] = [i.lhs() for i in prod]
    
    ##Iterations
    if solve:
        index = {}
        for prod in grammar.productions():
            index[prod.rhs()] = prod.lhs()

        for d in range(size_word):
            for i in range(size_word-d):
                j = i+d
                for k in range(i, j):
                    for B in cyk[i][k]:
                        for C in cyk[k+1][j]:
                            if (B,C) in index:
                                if cyk[i][j] == 'ø':
                                    cyk[i][j] = []
                                if index[(B,C)] not in cyk[i][j]:
                                    cyk[i][j].append(index[(B,C)])
    trace_cyk(cyk)
    try:
        return grammar.productions()[0].lhs() in cyk[0][size_word-1]
    except:
        return False

##Implementation of first algorithm for an LL parser
def first(grammar, solve=True):

    def add_first(x, y):
        add = False
        if eps not in index[y]:
            if index[x.lhs()] != {''}:
                t = index[x.lhs()]
                index[x.lhs()] = index[x.lhs()] | index[y]
                if index[x.lhs()] != t:
                    add = True
            else:
                index[x.lhs()] = index[y]
                add = True
        return add

    def trace_first(index):
        for key in index.keys():
            if not isinstance(key, str):
                print("First(" + str(key) + ") =",index[key])


    ##Init
    index = {}
    for prod in grammar.productions():
        if eps in list(prod.rhs()):
            index[prod.lhs()] = set([eps])
            
        c = prod.lhs()
        if c not in index:
            index[c] = set([''])

        for c in list(prod.rhs()):
            if isinstance(c, str):
                index[c] = set([c])

    ##Iteration
    if solve:
        add = True
        while(add):
            add = False
            for S in grammar.productions():
                r = list(S.rhs())

                ##First rule
                add = add_first(S, r[0]) or add ##If add is True, we need to keep it True

                ##Second rule
                for j in range(1, len(r)):
                    add_before = True
                    for i in range(j):
                        if eps not in index[r[i]]:
                            add_before = False
                            break
                    if add_before:
                        add = add_first(S, r[j]) or add ##If add is True, we need to keep it True

                ##Third rule
                add_eps = True
                for i in range(len(r)):
                    if eps not in index[r[i]]:
                        add_eps = False
                        break

                if add_eps:
                    if index[S.lhs()] != {''}:
                        t = index[S.lhs()]
                        index[S.lhs()] = index[S.lhs()] | {eps}
                        if index[S.lhs()] != t:
                            add = True
                    else:
                        index[S.lhs()] = {eps}
                        add = True
    trace_first(index)
    return index
    



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, help="the path of the text file containing the grammar")
    args = parser.parse_args()

    grammar = load_grammar(args.file)

    it = True
    while(it):
        it = False
        algo = input("Which algorithm do you want to use?\n").upper()

        if algo == "CYK":
            word = input("Type the word to analyze (or type eg to use the example)\n")
            if word == "eg":
                word = "the kids opened the box on the floor"
            print('\nCYK algorithm for',word,': \n')
            if CYK(grammar, word.split(), solve=True):
                print(word,"is in the grammar")
            else:
                print(word,"is not in the grammar")
        
        elif algo == "FIRST":
            print("\nThe first table for this grammar is: ")
            first(grammar,solve=True)
        
        else:
            print("Unknown algorithm. The algorithms currently implemented are: ")
            print("-CYK")
            print("-First")
            print('\n')
            it = True