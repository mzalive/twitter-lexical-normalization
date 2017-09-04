import fuzzy
import Levenshtein
import ngram
import time
import json
import os

token_path = 'data/labelled-tokens.txt'
dict_path = 'data/dict.txt'

def getDict():
    with open(dict_path, 'r') as dictFile:
        dictSet = [item.strip() for item in dictFile]
        return  dictSet


def match_levenshtein(token):
    dictSet = getDict()
    candidates = []
    candidatesG = []
    bestMatch = ""
    minDistance = 1

    for item in dictSet:
        distance = Levenshtein.distance(token.lower(), item.lower())
        if distance == 0:
            return item, [], []
        elif distance < minDistance:
            minDistance = distance
            candidates = []
        if distance == minDistance:
            candidates.append(item.lower())

    if len(candidates) > 1:
        G = ngram.NGram(candidates)
        candidatesG = G.search(token)
        bestMatch = candidatesG[0][0]
    elif len(candidates) == 1:
        bestMatch = candidates[0]

    return bestMatch, candidates, candidatesG


def match_soundex(token):
    dictSet = getDict()
    candidates = []
    candidatesG = []
    bestMatch = ""

    soundex = fuzzy.Soundex(8)
    soundex_token = soundex(token)

    candidates = [match for match in dictSet if soundex(match) == soundex_token]

    if len(candidates) > 1:
        G = ngram.NGram(candidates)
        candidatesG = G.search(token)
        bestMatch = candidatesG[0][0]
    elif len(candidates) == 1:
        bestMatch = candidates[0]

    return bestMatch, candidates, candidatesG


def match_double_metaphone(token):
    return


def execute(method):
    results = []
    count = 0
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

    with open('data/labelled-tokens.txt', 'r') as tokenFile:
        for tokenLine in tokenFile:
            count += 1
            tokenSet = tokenLine.split('\t')
            token = tokenSet[0].strip()
            code = tokenSet[1].strip()
            canonical = tokenSet[2].strip()

            best_match, candidates, candidatesG = target_method(token)

            result = {
                'token': token,
                'best_match': best_match,
                'candidates': candidates,
                'candidatesG': candidatesG,
                'canonical': canonical
            }

            results.append(result)
            print result

            if count == 10:
                break

    timestamp_end = time.time()
    time_elapse = timestamp_end - timestamp_start
    m, s = divmod(time_elapse, 60)

    output = {
        'benchmark': {
            'timestamp_start': time.ctime(timestamp_start),
            'timestamp_end': time.ctime(timestamp_end),
            'time_elapse': time_elapse,
            'time_elapse_readable': '%02d min %02d sec' % (m, s)
        },
        'results': results
    }

    if not os.path.isdir('output'):
        os.mkdir('output')

    with open('output/' + methodName + '.json', 'w') as fout:
        json.dump(output, fout)


execute(1)


