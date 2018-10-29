from agu_api import AguApi
from nltk.stem import WordNetLemmatizer

import nltk
import string
import math
import json
import re

# Year: CHANGE THIS PARAMETER TO LOAD DIFFERENT MEETINGS
year = 2017

# get an instance of the API
api = AguApi()

# get all the program ids in 2016
pIds = api.programsIds(year)

# download nltk dictionary
nltk.download('wordnet')

# get the lemmatizer instance to find the words root
lemmatizer = WordNetLemmatizer()

# find lemmas in the title for each abstract
abstracts = {}
a_ids = {}
for program_id in pIds:

    # store ids of each program_id
    a_ids[program_id] = []

    # get all the abstracts in 2016 in program_id
    raw_abstracts = api.abstracts(year, program_id)

    # some programs do not have abstracts
    if not raw_abstracts:
        print('NO ABSTRACTS FOR PID {}'.format(program_id))
        continue

    # post-process the abstracts
    for a in raw_abstracts:
        # all lower case and remove punctuation
        words = [w.lower().translate(str.maketrans({a:None for a in string.punctuation})) \
                        for w in re.split(' |\,|\-|\.|\;|\:', a['title'])]

        # find lemmas
        lemmas = [lemmatizer.lemmatize(word) for word in words]

        # save the lemmas for the abstract
        abstracts[a['abstractId']] = lemmas

        a_ids[program_id].append(a['abstractId'])

# compute occurencies of each lemma
dictionary = {}
for a_id in abstracts:
    for lemma in abstracts[a_id]:
        if lemma not in dictionary:
            dictionary[lemma] = 1
        else:
            dictionary[lemma] += 1

# filter dictionary
dictionary = {k: v for k, v in dictionary.items() if v>1}

sorted_dictionary = sorted(dictionary.items(), key=lambda t: t[1])

print("DICTIONARY INFO")
print("Number of words: {}".format(len(dictionary)))
print("Ten most used words: {}".format(', '.join('{}({})'.format(k,v) for k,v in sorted_dictionary[-10:])))
print("Ten least used words: {}".format(', '.join('{}({})'.format(k,v) for k,v in sorted_dictionary[:10])))


# build coefficients matrix for each program
for program_id in pIds:

    alpha = 0.01
    min_c = 0.1

    coeffs = {}
    # Debug
    # i = 1
    # j = 0
    # min_a = 1e9
    for a in a_ids[program_id]:
        coeffs[a] = {}
        for b in a_ids[program_id]:
            if a != b:
                if b in coeffs and a in coeffs[b]:
                    coeffs[a][b] = coeffs[b][a]
                else:
                    common_words = set(abstracts[a]) & set(abstracts[b])
                    if common_words:
                        coeff = 0.0
                        for w in common_words:
                            if w in dictionary:
                                coeff += math.exp(-alpha*dictionary[w])
                        if coeff > min_c:
                            coeffs[a][b] = coeff

        # Debug
        # min_a = min(min_a, len(coeffs[a]))
        # print(len(a_ids[program_id]), i, len(coeffs[a]), min_a, j, sep='\t')

        # if len(coeffs[a]) == 0:
        #     j += 1

        # i += 1

    file_name = 'graphs/coeffs_pid{}_alpha{}_minc{}.json'.format(
                                        program_id,
                                        str(alpha).replace('.', ''),
                                        str(min_c).replace('.', ''))
    with open(file_name, 'w') as f:
        json.dump(coeffs, f)
