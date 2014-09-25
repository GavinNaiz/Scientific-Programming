from __future__ import division
import nltk, glob
from nltk.probability import UniformProbDist
from collections import Counter as C
 
 
path = 'twitter-POS/'
 
# Other options exists. Change the number to 2, for no optimization, 3 for username optimization and 4 for hashtag optimization
# Case sensitivity is controlled on file load. simply remove ".lower()" where train and test variables are initialized
trainfile = 'train_google.txt'
testfile = 'test_google.txt'
 
 
def NLTK_HMM_parser(path, trainfile, testfile):
    def strip(l):
        nl = list([])
        for e in l:
            nl.append(e[0])
        return nl
 
    train = list(nltk.corpus.TaggedCorpusReader(path, trainfile, sep='|').tagged_sents())
 
    test = list(nltk.corpus.TaggedCorpusReader(path, testfile, sep='|').tagged_sents())
 
    hmmt = nltk.tag.HiddenMarkovModelTrainer()
    hmm = hmmt.train(labelled_sequences=train)
    print 'done training'
    (bl, cor, tot) = (0,0,0) # ????
    for t in test:
        print hmm.log_probability(t)
        ind = 0
        for e in hmm.tag(strip(t)):
            (word, pred) = e
            gold = t[ind][1]
            tot += 1
            ind += 1
            if pred == gold:
                cor += 1
    print "system:\t"+str(float(cor)/tot)+'\n'
 
#NLTK_HMM_parser(path, trainfile, testfile)
 
# Build start probabilities
 
train = open(glob.glob(path+trainfile)[0]).read().strip().lower().split('\n\n')
#train = open(glob.glob(path+trainfile)[0]).read().strip().split('\n\n')
 
taggedwords = C() # Counter for words
tags = C() # counter for tags / states
 
sp = C() # temporary counter for Start Probabilities
start_probabilities = {} #dictionary for Start Probabilities
 
emission_probabilities = {} # dictionary for emission probabilities
 
tp = C() #Counter for transmission probabilities
transmission_probabilities = {} #dictionary for Transmission probabilities
 
# count word/tag pairs and tags
 
for t in train:
    t = t.split('\n')
    sp += C([t[0].split('/')[1]])
    for w in t:
        word, tag = w.split('/')
        taggedwords +=C([w])
        tags += C([tag])
        emission_probabilities[word] = {}   # seed the emission probability dictinary of dictionaries
                                            # with an empty dictionary for every word
 
    for i in range(len(t)-1):
        basetag = t[i].split('/')[1]
        nexttag = t[i+1].split('/')[1]
        tagpair = basetag+'/'+nexttag
        tp += C([tagpair])
 
 
states = [t[0] for t in tags.items()]   # We could build these based on the 12 states
                                        # published in the google paper, but this way  
                                        # we build on the states observed
for s in states:
    for s2 in states:
        transmission_probabilities[s] = {s:0}   # Seed the transmission probability dictionary with zero
                                                # probabilities for all transmissions
 
# Build start probabilities
 
total = float(sum(sp.values()))
 
for i in sp.items():
    start_probabilities[i[0]] = i[1]/total
 
 
# Build emission (dict)
# _____________________
 
 
for w in taggedwords.items():
    word, tag = w[0].split('/')
    emission_probabilities[word][tag] = w[1] / tags[tag]
            # Creates a dictionary of dictionaries.
            # This is super messy, so be careful!
            # Basically this allows us to find emission probability for the noun dog as:
            # ep['dog']['noun']
 
 
# build transmission (dict)
# _________________________
 
# Nouns -> verb
#   How many times do I see a noun?
#   How many times is it followed by a verb?
#       #N,V / #N
 
for t in tp.items():
    basetag, nexttag = t[0].split('/')
 
    transmission_probabilities[basetag][nexttag] = float(t[1])/tags[basetag]
 
 
########################
### Define Functions ###
########################
  
 
def print_dptable(V):
    print "    ",
    for i in range(len(V)): print "%7s" % ("%d" % i),
    print
  
    for y in V[0].keys():
        print "%.5s: " % y,
        for t in range(len(V)):
            print "%.7s" % ("%f" % V[t][y]),
        print
 
def print_obs_targ(obs, targ):
    obs_out, targ_out = '',''
    for i in obs:
        obs_out += i+'\t'
    for i in targ:
        targ_out += i+'\t'
    print obs, "\n", targ
 
# visualize viterbi
# Modified from wikipedia
def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    path = {}
  
    # Initialize base cases (t == 0)
    # Begin calculating start probability for current tweet.
 
    for y in states:
        try:
            if emit_p[obs[0]]:
                ep = emit_p[obs[0]][y]
        except:
            ep = 0.000001 # We give every start position a chance. # lower than 0.00001 doesnt seem to improve results. Zero is bad, higher is generally bad too 
 
        V[0][y] = start_p[y] * ep
        path[y] = [y]
  
    # Run Viterbi for t > 0
    # Calculate rest of tweet
 
    for t in range(1,len(obs)):
        V.append({})
        newpath = {}
        has_emission = False
        try:
            if emit_p[obs[t]] != {} :   # if there is an emission probability for the current observation
                                        # then the current observation has at least one emission probability
                                        # for some state
                has_emission = True
        except:
            has_emission = False
 
        for y in states:
            try:                        # try at find the emission probability for the current observation and state
                ep = emit_p[obs[t]][y]
            except:
                if has_emission:    # if there is no emission probability for the current observation with the current state, 
                                    # but for some other tag, we set ep to low
                    ep = 0.00001
                else:           # If there is no emission probability for the current obs for any state, we make up a low ep, so the chain can complete
                    ep = 1  # seems to be the low end of actual probabilities
 
            (prob, state) = max([(V[t-1][y0] * trans_p[y0][y] * ep, y0) for y0 in states])
            V[t][y] = prob
            newpath[y] = path[state] + [y]
  
        # Don't need to remember the old paths
        path = newpath
  
    #print_dptable(V)
    (prob, state) = max([(V[len(obs) - 1][y], y) for y in states])
    return (prob, path[state])
 
def compare(targ, guess):
    correct = 0
    full_match = 0
    for i in range(len(targ)):
        if targ[i] == guess[i]:
            correct +=1
    if i+1 == correct:
        full_match = 1
    return correct, i+1, full_match
 
 
#########################
### Load observations ###
#########################
 
test = open(glob.glob(path+testfile)[0]).read().strip().lower().split('\n\n')
#test = open(glob.glob(path+testfile)[0]).read().strip().split('\n\n')
observations = []
targets = []
for t in test:
    t = t.split('\n')
    words, tags = [], []
    for w in t:
        word, tag = w.split('/')
        words.append(word)
        tags.append(tag)
    observations.append(words)
    targets.append(tags)
 
#
# Begin testing
#
 
correct, total, full_matches = 0,0,0
for i in range(len(observations)):
    prob, path = viterbi(observations[i], states, start_probabilities, 
                transmission_probabilities, emission_probabilities)
    c, t, f = compare(targets[i], path)
    correct += c
    total += t
    full_matches +=f
print 'correctly tagged words:', correct, '/', total, '=', float(correct)/total
print 'correctly sentences:', full_matches, '/', i+1, '=', float(full_matches)/(i+1)