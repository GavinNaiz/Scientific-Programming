from TwitterSearch import *

f = open("tweet.txt", "r+")

try: 
    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.setKeywords(['Hibernian', 'Edinburgh']) # let's define all words we would like to have a look for
    tso.setLanguage('en') # we want to see English tweets only
    tso.setCount(10) # please dear Mr Twitter, only give us 10 results per page
    tso.setIncludeEntities(False) # and don't give us all those entity information

    # it's about time to create a TwitterSearch object with our secret tokens
    ts = TwitterSearch(
        consumer_key = 'NS1Bdacglj3oRMOj2bxt1Q',
        consumer_secret = 'zFlMIVnqPgjg6pTpZUiZsG0GK1u47bH9hMR8UqeIChA',
        access_token = '20521933-J5TOcvlhx8DiakHiRrjCzvOtpxIAW5hT0F0O5vncb',
        access_token_secret = 'hlyuQl0AztXe2EY6sylYfQUARoZqe9Tly5Sv5ntaOezN9'
     )

    i = 0
    for i in range(10):
        for tweet in ts.searchTweetsIterable(tso): # this is where the fun actually starts :)
            tweet = '%s' % tweet['text'].encode('utf-8')
            f.write(tweet)
            f.write("\n\n")

    f.close()
   

except TwitterSearchException as e: # take care of all those ugly errors if there are some
    print(e)