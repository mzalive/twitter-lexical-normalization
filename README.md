# Twitter Lexical Normalisation
COMP90049 Knowledge Technologies, Semester 2 2017
<br>
Project 1 - Lexical Normalisation of Twitter Data

### Overview
This project is a python script that uses varieties of string matching method correct misspelled words.

Following methods are implemented in this project:

* Levenshtein Distance
* Soundex
* Double Metaphone
* Levenshtein Distance + Soundex

\* All the approach listed above are followed by a N-Gram Similarity evaluation as a tie-breaker to present a 'best_match' prediction.


### Usage
```
usage: main.py -m

   -m   method:
        0: Levenshtein
        1: Soundex
        2: Double Metaphone
        3: Levenshtein + Soundex
```

### Data Analysis
The analyse script accept a json file produced by the main.py and produces a brief analysis report.
```
$ python analyse.py output/levenshtein.json
```

### Credits

* [Levenshtein-python](https://github.com/ztane/python-Levenshtein)
* [python-ngram](https://github.com/gpoulter/python-ngram)
* [Fuzzy](https://github.com/yougov/fuzzy)
