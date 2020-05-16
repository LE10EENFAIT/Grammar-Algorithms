import nltk

def trace(cyk):
    for i in range(len(cyk)):
        print(cyk[i])

def load_grammar(filename):
    f = open(filename, 'r')
    return nltk.CFG.fromstring(f.read())

def CYK(grammar, word, solve=True):
    size_word = len(word)
    cyk = [['ø' for i in range(size_word)] for j in range(size_word)]

    for i in range(size_word):
        prod = grammar.productions(rhs=word[i])
        cyk[i][i] = [i.lhs() for i in prod]
    
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
                                cyk[i][j].append(index[(B,C)])
    trace(cyk)
    try:
        return grammar.productions()[0].lhs() in cyk[0][size_word-1]
    except:
        return False




if __name__ == "__main__":
    grammar = load_grammar('grammar.txt')
    algo = input("Which algorithm do you want to use?\n").upper()

    if algo == "CYK":
        word = input("Type the word to analyze (or type eg to use the example)\n")
        if word == "eg":
            word = "the kids opened the box on the floor"
        print('CYK algorithm for',word,': \n')
        if CYK(grammar, word.split(), solve=True):
            print(word,"is in the grammar")
        else:
            print(word,"is not in the grammar")