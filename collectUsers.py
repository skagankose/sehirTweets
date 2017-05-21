import tweepy
import json
import sys
import time
import csv
import numpy as np

# Twitter credentials
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
API = tweepy.API(auth)

# Read core users from the file
userNameList = []
f = open("data/coreUsers.txt", "rt")
for user in f:
    userNameList.append(user.strip("\n"))
f.close()

followersDict = dict()
followeesDict = dict()
for userName in userNameList:
    try:
        temporarySet = set()
        for userID in tweepy.Cursor(API.followers_ids, screen_name=userName).items():
            temporarySet.add(userID)
        followersDict[userName] = list(temporarySet)

        temporarySetV2 = set()
        for userID in tweepy.Cursor(API.friends_ids, screen_name=userName).items():
            temporarySetV2.add(userID)
        followeesDict[userName] = list(temporarySetV2)

    except Exception as error:
        print("Error : %s" % error)
        if str(error) == "[{'message': 'Rate limit exceeded', 'code': 88}]":
            time.sleep(61*15)
            try:
                temporarySet = set()
                for userID in tweepy.Cursor(API.followers_ids, screen_name=userName).items():
                    temporarySet.add(userID)
                followersDict[userName] = list(temporarySet)

                temporarySetV2 = set()
                for userID in tweepy.Cursor(API.friends_ids, screen_name=userName).items():
                    temporarySetV2.add(userID)
                followeesDict[userName] = list(temporarySetV2)
            except Exception as secondError:
                print("Error : %s" % secondError)


newFolloweesDict = dict()
newFollowersDict = dict()
for userName in followeesDict:
    followees = followeesDict[userName]
    followers = followersDict[userName]
    newKey = API.get_user(screen_name=userName).id
    newFolloweesDict[newKey] = followees
    newFollowersDict[newKey] = followers

# Save dictionaries
np.save('data/dictionary/followers.npy', newFollowersDict)
np.save('data/dictionary/followees.npy', newFolloweesDict)

IDList = set()
for i in newFolloweesDict:
    IDList.add(i)
    for ii in newFolloweesDict[i]:
        IDList.add(ii)
for j in newFollowersDict:
    IDList.add(j)
    for jj in newFollowersDict[j]:
        IDList.add(jj)
IDSet = set(IDList)

# Save graph nodes and edges
with open('data/graph/edges.csv', 'a') as out:

    writer = csv.writer(out, delimiter=',', lineterminator='\n')
    writer.writerow(['source', 'target', 'type', 'weight'])

    for userID in newFollowersDict:
        for followerID in newFollowersDict[userID]:
            writer.writerow([followerID, userID, 'Directed', 1])

    for userID in newFolloweesDict:
        for followeeID in newFolloweesDict[userID]:
            writer.writerow([userID, followeeID, 'Directed', 1])

with open('data/graph/nodes.csv', 'a') as out:

    writer = csv.writer(out, delimiter=',', lineterminator='\n')
    writer.writerow(['id'])

    for userID in IDSet:
        writer.writerow([userID])
