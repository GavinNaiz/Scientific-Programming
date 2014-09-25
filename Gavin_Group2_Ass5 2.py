import numpy as np
import sys
import os
from collections import Counter as C


"""
    Set up the files and lists
"""

# Open the file with tweets
fTweets = open('tweet.txt', 'r') # Open the raw tweets.
fAnnotated = open('annotated.txt', 'r+') # Open file with annotations (a = append to file).

tags = ['ADV', 'VERB', 'NOUN', 'ADP', 'PRON', 'DET', '.', 'PRT', 'NUM', 'X', 'CONJ', 'ADJ', 'EXIT']
tagString = "ADV, VERB, NOUN, ADP, PRON, DET, ., PRT, NUM, X, CONJ, ADJ"

tweetList = fTweets.read().split('\n\n')

wordList = [w.lower().split() for w in tweetList]

"""
    Our annotation tool.
    
    Annotated tweets are saved as 'word|tag;' so it doesn't conflict with many tweets.
"""
def annotateTweet(t):
  print "Tweet:"
  print "%s \n" % t
  t = t.split()
  annotatedTweet = ""
  for w in t:
    check = False
    print w

    while check == False:
      uInput = raw_input("Tag the word: ")

      if uInput == "EXIT":
        userMenu()

      elif uInput in tags:
        tmp = '%s\t%s\n' % (w, uInput)
        check = True

    annotatedTweet += tmp

  annotatedTweet += "\n\n"
  print "All words in tweet annotated and saved to file."  
  fAnnotated.write(annotatedTweet)

  os.system('clear')
  return annotatedTweet

def annotate():
  print "Here we annotate tweets from Twitter.com.\n"

  print "Allowed tags: %s" % tagString
  print "Quit by typing EXIT"

  for t in tweetList:
    tmp = annotateTweet(t)


def userMenu():
  os.system('clear')
  print "Annotation of Tweets.\n"
  print "1. Annotate"
  print "2. Use tool"
  print "3. Quit!\n"
  tmp = raw_input("Select what to do: ")

  if tmp == "1":
    os.system('clear')
    annotate()

  elif tmp == "2":
    os.system('clear')
    tagTool()

  elif tmp == "3":
    print "\nGood bye."
    sys.exit()

  else:
    userMenu()

# Run
userMenu()
fTweets.close()
fAnnotated.close()
tntSave.close()