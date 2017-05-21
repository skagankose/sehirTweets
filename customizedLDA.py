from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# To clean stopwords
stopFile = open("data/stopWords/turkish.txt", 'r')
allStop = list()
for stopWord in stopFile:
    if stopWord != '\n':
        allStop += [stopWord.strip("\n").strip(" ").strip("\t")]
stopFile.close()

# To remove english words
englishFile = open("data/stopWords/english.txt", 'r')
englishWords = list()
for englishWord in englishFile:
    if englishWord != '\n':
        englishWords += [englishWord.strip("\n").strip(" ").strip("\t")]
englishFile.close()

allStop += ["cok", "icin", "bi", "im", "https", "la", "bak", "slam", "dr",
            "falan", "mi", "evet", "ye", "ka", "lan", "yav", "aq", "ol", "rde",
            "amp", "size", "ran", "şte", "ey", "sn", "şehi", "ürk", "lar",
            "sayın", "abi", "tl", "cok", "icin", "bi", "im", "https", "la",
            "bak", "slam", "dr", "falan", "mi", "evet", "ye", "ka", "lan",
            "yav", "aq", "ol", "rde", "sayın", "abi", "tl", 'https', 'nü', "pr",
            "amp", "size", "ran", "şte", "ey", "sn", "şehi",
            "ürk", "lar", "ta"] + englishWords
stopSet = set(allStop)

# Load tweets within STN
tweetFile = open("data/allTweets.txt", 'r')
tweetList = list()
for tweet in tweetFile:
    if tweet != "\n":
        tweetList += [tweet.replace("i̇","i")]

# Parameters for LDA
nSamples = len(tweetList)
nFeatures = 1000
nTopics = 4
nTopWords = 20

def printTopWords(model, feature_names, nTopWords):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-nTopWords - 1:-1]]))
    print()

# Use TF (raw term count) features for LDA.
TFVectorizer = CountVectorizer(max_df=0.95, min_df=2,
                                max_features=nFeatures,
                                stop_words=stopSet)
TF = TFVectorizer.fit_transform(tweetList)

# Fit the LDA model
LDA = LatentDirichletAllocation(n_topics=nTopics, max_iter=5,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0)
LDA.fit(TF)
TFFeatureNames = TFVectorizer.get_feature_names()
printTopWords(LDA, TFFeatureNames, nTopWords)
