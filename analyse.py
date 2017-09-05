import json
import sys
import os

if len(sys.argv) < 2:
    print 'Please specify input json file'
    exit()

filepath = sys.argv[1]
if not os.path.exists(filepath):
    print "File/dir doesn't exist"
    exit()

directory = os.path.dirname(filepath)
if len(directory) > 0:
    directory += '/'
basename = os.path.basename(filepath)
filename = os.path.splitext(basename)[0]

with open(filepath, 'r') as fin:
    data = json.load(fin)

    results = data['results']

    time = int(data['benchmark']['time_elapse'])
    time_readable = data['benchmark']['time_elapse_readable']

    count_total = len(results)
    count_total_candidates = 0
    count_has_match = 0
    count_hit = 0

    for result in results:
        best_match = result['best_match']
        canonical = result['canonical']
        candidates = result['candidates']

        if len(candidates) == 0 and best_match == canonical:
            count_hit += 1
            count_has_match += 1
            count_total_candidates += 1
            continue
        if len(candidates) > 0 and canonical in candidates:
            count_has_match += 1
            count_total_candidates += len(candidates)
            if best_match == canonical:
                count_hit += 1

    recall = count_has_match / float(count_total)
    precision = count_has_match / float(count_total_candidates)
    accuracy = count_hit / float(count_total)


with open(directory + filename + '-analysis' + '.out', 'w') as fout:
    fout.write('Time: %s (%d sec)\n' %(time_readable, time))
    fout.write('Total: %d entries processed.\n' %count_total)
    fout.write('%d hits, %d entries have correct suggestion, %d total suggestions\n' %(count_hit, count_has_match, count_total_candidates))
    fout.write('Precision: %f\nRecall: %f\nAccuracy: %f' %(precision, recall, accuracy))

