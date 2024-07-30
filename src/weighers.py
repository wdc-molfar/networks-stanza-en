# weighers.py

import sys
from nltk import FreqDist

def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k

def time_series(allTermsTagsGTF, sentsTermsTags):
    sentTseries = []
    sentsTseries = []
    sentTuples = []
    sentsTuples = []
    i = 0
    for sentTermsTags in sentsTermsTags:
        for termTag in sentTermsTags:
            sentTseries.append(allTermsTagsGTF[i][2])
            sentTuples.append((allTermsTagsGTF[i][0], allTermsTagsGTF[i][1], allTermsTagsGTF[i][2]))
            i = i + 1
        sentsTseries.append(sentTseries)
        sentsTuples.append(sentTuples)
    return sentsTseries, sentsTuples

def tuples_builder(allTermsTags):
    allTermsTagsGTF = allTermsTags.copy()
    sys.stdout = sys.__stdout__
    gtfDist = FreqDist(word for word in allTermsTags)
    for (termtag, freq) in gtfDist.most_common():
        # return all indexes (positions) of "termtag" in "allTermsTagsGTF"
        indexes = [index for index, value in enumerate(allTermsTagsGTF) if value == termtag]
        for i in indexes:
            allTermsTagsGTF[i] = (termtag[0], termtag[1], freq)
    return allTermsTagsGTF
    