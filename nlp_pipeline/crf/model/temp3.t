# Unigram

# Word +bigrams
U00:%x[-2,0]
U01:%x[-1,0]
U02:%x[0,0]
U03:%x[1,0]
U04:%x[2,0]
U05:%x[-1,0]/%x[0,0]
U06:%x[0,0]/%x[1,0]

# Lemma +bigrams
U10:%x[-2,1]
U11:%x[-1,1]
U12:%x[0,1]
U13:%x[1,1]
U14:%x[2,1]
U15:%x[-1,1]/%x[0,1]
U16:%x[0,1]/%x[1,1]

# POS +bigrams,trigrams
U20:%x[-2,2]
U21:%x[-1,2]
U22:%x[0,2]
U23:%x[1,2]
U24:%x[2,2]
U25:%x[-2,2]/%x[-1,2]
U26:%x[-1,2]/%x[0,2]
U27:%x[0,2]/%x[1,2]
U28:%x[1,2]/%x[2,2]
U200:%x[-2,2]/%x[-1,2]/%x[0,2]
U201:%x[-1,2]/%x[0,2]/%x[1,2]
U202:%x[0,2]/%x[1,2]/%x[2,2]

# MeSH +bigrams,trigrams
U30:%x[-2,3]
U31:%x[-1,3]
U32:%x[0,3]
U33:%x[1,3]
U34:%x[2,3]
U35:%x[-2,3]/%x[-1,3]
U36:%x[-1,3]/%x[0,3]
U37:%x[0,3]/%x[1,3]
U38:%x[1,3]/%x[2,3]
U300:%x[-2,3]/%x[-1,3]/%x[0,3]
U301:%x[-1,3]/%x[0,3]/%x[1,3]
U302:%x[0,3]/%x[1,3]/%x[2,3]

# Drug names +bigrams
U40:%x[-2,4]
U41:%x[-1,4]
U42:%x[0,4]
U43:%x[1,4]
U44:%x[2,4]
U45:%x[-1,4]/%x[0,4]
U46:%x[0,4]/%x[1,4]

# Headers
U50:%x[0,5]


# Bigram
B
