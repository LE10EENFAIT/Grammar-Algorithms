import nltk
import argparse

eps = 'ε'
dollar = '$'

def load_grammar(filename):
    f = open(filename, 'r')
    return nltk.CFG.fromstring(f.read())

def trace_index(index, msg):
        for key in index.keys():
            if not isinstance(key, str):
                print(msg + "(" + str(key) + ") = {", end='')

                for i in range(len(index[key])):
                    if i < len(index[key]) - 1:
                        print(list(index[key])[i], end=', ')
                    else:
                        print(list(index[key])[i], end='')
                print('}')

##Implementation of CYK algorithm
def CYK(grammar, word, solve=True):

    def trace_cyk(cyk):
        for i in range(len(cyk)):
            print(cyk[i])

    ##Initialisation
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

##Implementation of First algorithm for an LL parser
def First(grammar, solve=True, trace=True):

    def add_els(x, els, remove_eps=True):
        temp1 = premier[x.lhs()].copy()
        temp2 = els.copy()
        if remove_eps:
            if eps in temp2:
                temp2.remove(eps)
        premier[x.lhs()] = premier[x.lhs()] | temp2
        if premier[x.lhs()] != temp1:
            return True
        return False

    ##Initialisation
    premier = {}
    for prod in grammar.productions():
        premier[prod.lhs()] = set()

        if eps in list(prod.rhs()):
            premier[prod.lhs()] |= set([eps])
            
        for c in list(prod.rhs()):
            if isinstance(c, str):
                premier[c] = set([c])

    ##Iterations
    if solve:
        add = True
        while(add):
            add = False
            for S in grammar.productions():
                r = list(S.rhs())

                ##First rule
                add += add_els(S, premier[r[0]])

                ##Third rule
                add_eps = True
                for i in range(len(r)):
                    if eps not in premier[r[i]]:
                        add_eps = False
                        break

                if add_eps:
                    add += add_els(S, {eps}, remove_eps=False)

                else:
                    ##Second rule
                    for j in range(1, len(r)):
                        add_before = True
                        for i in range(j):
                            if eps not in premier[r[i]]:
                                add_before = False
                                break
                        if add_before:
                            add += add_els(S, premier[r[j]])
                

    if trace:
        trace_index(premier, "First")
    return premier

##Implementation of Follow algorithm for an LL parser
def Follow(grammar, trace=True):

    def add_els(x, els):
        temp1 = suivant[x].copy()
        temp2 = els.copy()

        if eps in temp2:
            temp2.remove(eps)

        suivant[x] = suivant[x] | temp2
        if suivant[x] != temp1:
            return True
        return False

    def decompose_aMb(W):
        res = []
        for i in range(len(W)):
            if not isinstance(W[i], str) and i < len(W) - 1:
                a = W[:i]
                M = W[i]
                B = W[i+1:]
                if a == []:
                    a = eps
                res.append([a,M,B])
        return res

    ##Initialisation
    suivant = {}

    for prod in grammar.productions():
        suivant[prod.lhs()] = set()
        for c in list(prod.rhs()):
            if isinstance(c, str):
                suivant[c] = set([c])
    suivant[grammar.productions()[0].lhs()] = set([dollar])

    ##Iteration
    premier = First(grammar, trace=False)
    add = True
    while(add):
        add = False
        for S in grammar.productions():
            
            ##First decomposition
            decompositions = decompose_aMb(list(S.rhs()))
            for decomposition in decompositions:
                ##First rule
                if isinstance(decomposition[2][0], str):
                    add += add_els(decomposition[1], set([decomposition[2][0]]))
                else:
                    add += add_els(decomposition[1], premier[decomposition[2][0]])

                    ##Second rule
                    if eps in premier[decomposition[2][0]]:
                        add += add_els(decomposition[1], suivant[S.lhs()])

            ##Second decomposition
            rhs = list(S.rhs())        
            add = add_els(rhs[len(rhs)-1], suivant[S.lhs()]) or add

    if trace:
        trace_index(suivant, "Follow")
    
    return suivant





if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, help="the path of the text file containing the grammar", required=True)
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
            print("\nThe First sets for this grammar are: ")
            First(grammar,solve=True, trace=True)
        
        elif algo == "FOLLOW":
            print("\nThe Follow sets for this grammar are: ")
            Follow(grammar,trace=True)
        
        else:
            print("Unknown algorithm. The algorithms currently implemented are: ")
            print("- CYK")
            print("- First")
            print('- Follow')
            print('\n')
            it = True