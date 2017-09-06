import fuzzy
import Levenshtein
import ngram
import time
import json
import os
import sys

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
    minDistance = 3

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
        if len(candidatesG) > 0:
            bestMatch = candidatesG[0][0]
    elif len(candidates) == 1:
        bestMatch = candidates[0]

    return bestMatch, candidates, candidatesG


def match_soundex(token):
    dictSet = getDict()
    candidates = []
    candidatesG = []
    bestMatch = ""

    soundex = fuzzy.Soundex(4)
    soundex_token = soundex(token)

    candidates = [match for match in dictSet if soundex(match) == soundex_token]

    if len(candidates) > 1:
        G = ngram.NGram(candidates)
        candidatesG = G.search(token)
        if len(candidatesG) > 0:
            bestMatch = candidatesG[0][0]
    elif len(candidates) == 1:
        bestMatch = candidates[0]

    return bestMatch, candidates, candidatesG


def match_double_metaphone(token):
    dictSet = getDict()
    candidates = []
    candidatesG = []
    class1 = []
    class2 = []
    class3 =[]
    hasClass1 = False
    hasClass2 = False
    bestMatch = ""

    dmeta = fuzzy.DMetaphone()
    dm_token = dmeta(token)
    dm_token_pk = dm_token[0]
    dm_token_sk = dm_token[1]

    for match in dictSet:
        dm_match = dmeta(match)
        dm_match_pk = dm_match[0]
        dm_match_sk = dm_match[1]

        if (dm_token_pk != 'None') and (dm_token_pk == dm_match_pk):
            hasClass1 = True
            class1.append(match)
            continue
        if (not hasClass1) and ((dm_token_pk != 'None' and dm_token_pk == dm_match_sk)
                                or (dm_token_sk != 'None' and dm_token_sk == dm_match_pk)) :
            hasClass2 = True
            class2.append(match)
            continue

        if (not hasClass2) and (dm_token_sk != 'None' and dm_token_sk == dm_match_sk):
            class3.append(match)

    if hasClass1:
        candidates = class1
    elif hasClass2:
        candidates = class2
    else:
        candidates = class3

    if len(candidates) > 1:
        G = ngram.NGram(candidates)
        candidatesG = G.search(token)
        if len(candidatesG) > 0:
            bestMatch = candidatesG[0][0]
    elif len(candidates) == 1:
        bestMatch = candidates[0]

    return bestMatch, candidates, candidatesG

def match_levenshtein_soundex(token):
    dictSet = getDict()
    candidates = []
    candidatesG = []
    bestMatch = ""
    minDistance = 3

    for item in dictSet:
        distance = Levenshtein.distance(token.lower(), item.lower())
        if distance == 0:
            return item, [], []
        elif distance < minDistance:
            minDistance = distance
            candidates = []
        if distance == minDistance:
            candidates.append(item.lower())

    soundex = fuzzy.Soundex(4)
    soundex_token = soundex(token)

    soudex_candidates = [match for match in candidates if soundex(match) == soundex_token]

    if len(soudex_candidates) != 0:
        candidates = soudex_candidates

    if len(candidates) > 1:
        G = ngram.NGram(candidates)
        candidatesG = G.search(token)
        if len(candidatesG) > 0:
            bestMatch = candidatesG[0][0]
    elif len(candidates) == 1:
        bestMatch = candidates[0]

    return bestMatch, candidates, candidatesG

def execute(method):
    results = []

    if method == "0":
        methodName = 'levenshtein'
        target_method = match_levenshtein
    elif method == "1":
        methodName = 'soundex'
        target_method = match_soundex
    elif method == "2":
        methodName = 'double_metaphone'
        target_method = match_double_metaphone
    else:
        methodName = 'levenshtein_soundex'
        target_method = match_levenshtein_soundex

    print methodName
    timestamp_start = time.time()

    with open(token_path, 'r') as tokenFile:
        for tokenLine in tokenFile:
            tokenSet = tokenLine.split('\t')
            token = unicode(tokenSet[0].strip(), errors='ignore').encode()
            code = tokenSet[1].strip()
            canonical = unicode(tokenSet[2].strip(), errors='ignore').encode()

            if code != 'OOV':
                continue

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


if len(sys.argv) < 2:
    print 'Please specify method:\n' \
          '0: Levenshtein\n' \
          '1: Soundex\n' \
          '2: Double Metaphone\n' \
          '3: Levenshtein + Soundex'
    exit()

method = sys.argv[1]
execute(method)