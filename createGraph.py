import tweepy
import snap
import numpy as np
import csv

# Load API
consumer_key = "IivwDls7fYU6WTdzatJGxJ4Re"
consumer_secret = "xwsedLJdvvgT3EaMQwPA24LtYb4067EE2avf3ogCxyfRGJ0kCw"
access_token = "4590451846-yWybwxLHOGCpCwEmh5XgqcWgIbi505UvjJ1nP0y"
access_token_secret = "EWq727mJBVid759fqKJWVOacHYqYX4he1AVOeGV7cwkj6"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

API = tweepy.API(auth)

# Load followers and followee dictionaries, pre-saved
followerDictionary = np.load('data/dictionary/followers.npy').item()
followeeDictionary = np.load('data/dictionary/followees.npy').item()


# This whole code just removes all the users
# who had less than 3 followers and 3 followees
generalFollower = dict()
generalFollowee = dict()

for coreUser in followerDictionary:
    for otherUser in followerDictionary[coreUser]:
        if otherUser in generalFollowee:
            generalFollowee[otherUser] += [coreUser]
        else:
            generalFollowee[otherUser] = [coreUser]

for coreUser in followeeDictionary:
    for otherUser in followeeDictionary[coreUser]:
        if otherUser in generalFollower:
            generalFollower[otherUser] += [coreUser]
        else:
            generalFollower[otherUser] = [coreUser]

filteredFollower = dict()
for userID in  generalFollower:
    if len(generalFollower[userID]) > 2:
        filteredFollower[userID] = generalFollower[userID]

filteredFollowee = dict()
for userID in  generalFollowee:
    if len(generalFollowee[userID]) > 2:
        filteredFollowee[userID] = generalFollowee[userID]

updatedFilteredFollowee = dict()
for userID in  filteredFollowee:
    try:
        followerCount = filteredFollower[userID]
    except:
        followerCount = 0
    if followerCount > 2:
        updatedFilteredFollowee[userID] = filteredFollowee[userID]

updatedFilteredFollower = dict()
for userID in  filteredFollower:
    try:
        followeeCount = filteredFollowee[userID]
    except:
        followeeCount = 0
    if followeeCount > 2:
        updatedFilteredFollower[userID] = filteredFollower[userID]

IDsList = list()
for anID in updatedFilteredFollower:
    IDsList.append(anID)
    for anotherID in updatedFilteredFollower[anID]:
        IDsList.append(anotherID)
for anID in updatedFilteredFollowee:
    IDsList.append(anID)
    for anotherID in updatedFilteredFollowee[anID]:
        IDsList.append(anotherID)
IDs = set(IDsList)

# Create CSV files for nodes and edges
with open('data/graph/node.csv', 'a') as outcsv:
    writer = csv.writer(outcsv, delimiter=',', lineterminator='\n')
    writer.writerow(['', 'id', 'label'])

    for (index, anID) in enumerate(IDs):

        print("Index : %d" % index)
        if index > 899 and index < 1035:

            try:
                userName = API.get_user(anID).screen_name
            except Exception as error:
                print("Error : %s" % error)
                userName = "n/a"
            writer.writerow([index, anID, userName])

with open('data/graph/edge.csv', 'a') as outcsv:
    writer = csv.writer(outcsv, delimiter=',', lineterminator='\n')
    writer.writerow(['source', 'target', 'type', 'weight'])

    for userID in updatedFilteredFollower:
        for followerID in updatedFilteredFollower[userID]:
            writer.writerow([followerID, userID, 'Directed', 1])

    for userID in updatedFilteredFollowee:
        for followeeID in updatedFilteredFollowee[userID]:
            writer.writerow([userID, followeeID, 'Directed', 1])
