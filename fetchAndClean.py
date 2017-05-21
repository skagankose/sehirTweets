import tweetDumper
import tweetCleaner

inputFile = open('data/graph/node.csv', 'rt')

reader = csv.reader(inputFile)

for (index, line) in enumerate(reader):
    userName = line[2]
    print("User : %s" % userName)
    if userName != "n/a":
        try:
            tweetDumper.getAllTweets(userName)
            tweetCleaner.clean(userName)
            print("Index : %s" % str(index + 1))

        except Exception as error:

            print("Error : %s" % error)

            if str(error) == "[{'code': 131, 'message': 'Internal error'}]":
                while True:
                    try:
                        tweetDumper.getAllTweets(userName)
                        tweetCleaner.clean(userName)
                        print("Done")
                        print("Index : %s" % str(index + 1))
                        break
                    except Exception as error:
                        print("Fetching user tweets...")
