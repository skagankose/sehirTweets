import re
import sys
import tweepy
import csv
import regex
import operator
import numpy as np
import preprocessor as pre


def cleanRT(aTweet):
    print(aTweet[:3] == "rt ")

def clean(userName):

    # Clean stopwords
    stopFile = open("data/stopWords/turkish.txt", 'r')
    allStop = list()
    for stopWord in stopFile:
        if stopWord != '\n':
            allStop += [stopWord.strip("\n").strip(" ").strip("\t")]
    stopFile.close()

    # Remove english tweets
    englishFile = open("data/stopWords/english.txt", 'r')
    englishWords = list()
    for englishWord in englishFile:
        if englishWord != '\n':
            englishWords += [englishWord.strip("\n").strip(" ").strip("\t")]
    englishFile.close()

    allStop += ["cok", "icin", "bi", "im", "https", "la", "bak", "slam", "dr",
                "falan", "mi", "evet", "ye", "ka", "lan", "yav", "aq", "ol", "rde",
                "amp", "size", "ran", "şte", "ey", "sn", "şehi", "ürk", "lar",
                "sayın", "abi", "tl", 'https', 'nü', "pr", "ta"] + englishWords
    stopSet = set(allStop)


    inputFile = open('data/raw/%s_tweets.csv' % userName, 'rt')
    outputFile = open('data/clean/%s_cleaned.csv' % userName, 'wt')

    pre.set_options(pre.OPT.URL, pre.OPT.EMOJI, pre.OPT.SMILEY,
                  pre.OPT.MENTION, pre.OPT.HASHTAG)
    reader = csv.reader(inputFile)
    writer = csv.writer(outputFile)

    for line in reader:
        label = line[0]
        text = line[1]
        currentString = str()
        for word in pre.clean(text).lower().split():
            cleanedWord = regex.sub(u'[^\p{Latin}]', u'', word)
            if cleanedWord not in stopSet:
                currentString += cleanedWord + " "
        currentString = currentString[3:] if currentString[:3 ] == "rt " else currentString
        if currentString.strip():
            writer.writerow((label, currentString.strip()))

    inputFile.close()
    outputFile.close()
