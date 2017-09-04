import fuzzy
import ngram
import time

token_path = 'data/labelled-tokens.txt'
dict_path = 'data/dict.txt'

def getDict():
    dictFile = open(dict_path, 'r')
    dictSet = [item.strip() for item in dictFile]
    return  dictSet

def match_levenshtein(token):
    return

def match_soundex(token):
    return

def match_double_metaphone(token):
    return

def execute(method):
    tokenFile = open('data/labelled-tokens.txt', 'r')

    if method == 0:
        methodName = 'levenshtein'
        target_method = match_levenshtein
    elif method == 1:
        methodName = 'soundex'
        target_method = match_soundex
    else:
        methodName = 'double_metaphone'
        target_method = match_double_metaphone

    timestamp_start = time.time()

    for tokenLine in tokenFile:
        tokenSet = tokenLine.split('\t')
        token = tokenSet[0].strip()
        code = tokenSet[1].strip()
        canonical = tokenSet[2].strip()

        # best_match, candidates = target_method(token)

        # handle result

    timestamp_end = time.time()
    time_elapse = timestamp_end - timestamp_start





