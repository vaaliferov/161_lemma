def get_stem(words):

    stem = ''

    if len(words) == 0: return ''
    if len(words[0]) == 0: return ''
    if len(words) == 1: return words[0]

    c = lambda s: all(s in x for x in words)

    for i in range(len(words[0])):
        for j in range(len(words[0])-i+1):
            if j > len(stem) and c(words[0][i:i+j]):
                stem = words[0][i:i+j]

    return stem

def get_prefixes(words, stem):
    return [w[:w.index(stem)] for w in words]

def get_suffixes(words, stem):
    return [w[w.index(stem)+len(stem):] for w in words]