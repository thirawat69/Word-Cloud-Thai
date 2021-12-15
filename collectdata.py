import pymongo
from pymongo import MongoClient
import json
import tweepy
import twitter
from pprint import pprint
import configparser
import pandas as pd
import certifi

def cullecttweet( q, count):

    # Load the Authorization Info
    config = configparser.ConfigParser()
    config.read('config.ini')

    CONSUMER_KEY      = config['mytwitter']['api_key']
    CONSUMER_SECRET   = config['mytwitter']['api_secrete']
    OAUTH_TOKEN       = config['mytwitter']['access_token']
    OATH_TOKEN_SECRET = config['mytwitter']['access_secrete']
    mongod_connect    = config['mymongo']['connection']



    # Connect to the MongoDB Cluster
    ca = certifi.where()                                 # Fix SSR error

    client = MongoClient(mongod_connect , tlsCAFile=ca)  # connect to mongo and fix SSL problem with tlsCAFile=ca
    db = client.Twitter                                  # use or create a database named Twitter
    tweet_collection = db.new_tweet_collection           # use or create a collection named tweet_collection



    # Authorize the Stream API
    stream_auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    stream_auth.set_access_token(OAUTH_TOKEN, OATH_TOKEN_SECRET)

    strem_api = tweepy.API(stream_auth)



    # Authorize the REST API 
    rest_auth = twitter.oauth.OAuth(OAUTH_TOKEN,OATH_TOKEN_SECRET,CONSUMER_KEY,CONSUMER_SECRET)
    rest_api = twitter.Twitter(auth=rest_auth)



    # Define the query for the REST API
    #count = 10                                  # number of returned tweets
    #q = "#ผู้ว่ากทม"                               # define the keywords, tweets contain election
    geocode = "38.4392897,-78.9412224,50mi"      # defin the location, in Harrisonburg, VA



    # Search and Collect data
    start = tweet_collection.count_documents({}) # จำนวนคอลเลกชั่นที่มีในปัจจุบัน
    since_id_old = start
    since_id_new = start+count
    i=1

    while(since_id_new != since_id_old):
        search_results = rest_api.search.tweets( count=count,q=q) #you can use both q and geocode
        statuses = search_results["statuses"]

        for statuse in statuses:
            try:# time sleep to slow request
                if tweet_collection.count_documents({})%100==0:
                    time.sleep(5)
                # fetching the status
                tweet = strem_api.get_status(statuse['id_str'], tweet_mode = "extended")
                
                # fetching the text attribute
                full_text  = tweet.full_text  

                # collection stucture
                new_tweet = {
                    'id_doc': since_id_old,
                    'id_str': statuse['id_str'],
                    'keyword': q,
                    'full_text': full_text,
                }
                
                # make sure the collected tweets are unique
                abc = tweet_collection.find_one({'id_str': statuse['id_str']})
                if abc==None:
                    # insert tweet
                    tweet_collection.insert_one(new_tweet)
                    print("The text of the status is \n:" + full_text )
                    print(i, "documents insert\n\n")
                    i=i+1
                    since_id_old=since_id_old+1
                else:
                    print("same data in collection")       
                
            except:
                pass



    # Pull data form tweet_collection to variable tweet_json
    tweet_json = list(tweet_collection.find())


    # collect all word that cut uaeless word
    all_tweet = ""
    for i in range(tweet_collection.count_documents({})):
        all_tweet += cutword(tweet_json[i]['full_text'])+"\n"


    # drop collection
    tweet_collection.drop()
    
    return(all_tweet)




def cutword(wordinput):
    wordmodify = wordinput+"`"

    #ตัดชื่อคน รีทวิต
    Tweet = wordmodify.find("RT") 
    endnameTweet = wordmodify.find(":")
    substring = wordmodify[Tweet:endnameTweet+1]
    # print(substring)

    cutTweet=wordmodify.replace(substring,"")
    # print(cutTweet)

    #ตัดหลัง https
    https = cutTweet.find("https://t.co") 
    endpoint = cutTweet.find("`")
    substring = cutTweet[https:endpoint+1]
    # print(substring)

    aa=cutTweet.replace(substring,"")
    # print(aa)
    return aa