# nlprocessing.py

def stanza_built_words(sent, TermsTags, stopWords):
    WordsTags = []
    for word in sent.words:
        try:
            nword = word.lemma
            tag = word.upos
        except:
            continue
        if tag == 'PROPN':
            tag = 'NOUN'
        WordsTags.append((nword,tag))
        if (nword not in stopWords) and (tag == 'NOUN'): 
            TermsTags.append((nword, tag))
    return TermsTags, WordsTags

def stanza_built_bigrams(WordsTags, TermsTags, stopWords):
    for i in range(1, len(WordsTags)):
        w1 = WordsTags[i-1][0] 
        w2 = WordsTags[i][0]
        t1 = WordsTags[i-1][1]
        t2 = WordsTags[i][1]
        if (t1 == 'ADJ') and (t2 == 'NOUN') and (w1 not in stopWords) and (w2 not in stopWords):
            TermsTags.insert([index for index, value in enumerate(TermsTags) if value == (w2,t2)][-1], (w1+'~'+w2, t1+'~'+t2))
    return TermsTags

def stanza_built_threegrams(WordsTags, TermsTags, stopWords):
    for i in range(2, len(WordsTags)):
        w1 = WordsTags[i-2][0]
        w2 = WordsTags[i-1][0]
        w3 = WordsTags[i][0]
        t1 = WordsTags[i-2][1]
        t2 = WordsTags[i-1][1]
        t3 = WordsTags[i][1]
        if (t1 == 'NOUN') and ((t2 == 'CCONJ') or (t2 == 'ADP')) and (t3 == 'NOUN') and (w1 not in stopWords) and (w3 not in stopWords):
            TermsTags.insert([index for index, value in enumerate(TermsTags) if value == (w1,t1)][-1], (w1+'~'+w2+'~'+w3, t1+'~'+t2+'~'+t3))
        elif (t1 == 'ADJ') and (t2 == 'ADJ') and (t3 == 'NOUN') and (w1 not in stopWords) and (w2 not in stopWords) and (w3 not in stopWords):
            TermsTags.insert([index for index, value in enumerate(TermsTags) if value == (w2+'~'+w3,t2+'~'+t3)][-1], (w1+'~'+w2+'~'+w3, t1+'~'+t2+'~'+t3))
    return TermsTags

def stanza_nlp(text, nlpModel, stopWords):
    TermsTags = []
    sentsTermsTags = [] #list of targed sentenses (list of lists of targed words)
    allTermsTags = [] #list of all targed words without division into sentences (only NOUN) 
    doc = nlpModel(text)
    sents = doc.sentences
    for sent in sents:
        TermsTags, WordsTags = stanza_built_words(sent, TermsTags, stopWords)
        if (len(WordsTags)>2):
            TermsTags = stanza_built_bigrams(WordsTags, TermsTags, stopWords)
        if (len(WordsTags)>3):
            TermsTags = stanza_built_threegrams(WordsTags, TermsTags, stopWords)
        allTermsTags = allTermsTags + [wt for wt in TermsTags] 
        sentsTermsTags.append(TermsTags)
        TermsTags = []
    return allTermsTags, sentsTermsTags
