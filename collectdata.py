import pymongo
from pymongo import MongoClient

import tweepy
import twitter

import configparser

import certifi
from pythainlp import word_tokenize
from pythainlp.corpus import get_corpus # for getting stopwords

from wordcloud import WordCloud

import matplotlib.pyplot as plt
import numpy as np

def collecttweet( keywords, max_tweets):
    # Load the Authorization Info
    # Save database connection info and API Keys in a config.ini file and use the configparse to load the authorization info.
    config = configparser.ConfigParser()
    config.read('config.ini')

    CONSUMER_KEY      = config['mytwitter']['api_key']
    CONSUMER_SECRET   = config['mytwitter']['api_secrete']
    OAUTH_TOKEN       = config['mytwitter']['access_token']
    OATH_TOKEN_SECRET = config['mytwitter']['access_secrete']

    mongod_connect = config['mymongo']['connection']

    # Connect to the MongoDB Cluster 
    # the name database and collection is here.

    ca = certifi.where()                                 # Fix SSR error

    client = MongoClient(mongod_connect , tlsCAFile=ca)  # connect to mongo and fix SSL problem with tlsCAFile=ca
    db = client.Twitter                                  # use or create a database named Twitter
    tweet_collection = db.new_tweet_collection           # use or create a collection named tweet_collection

    # Setup tweepy to authenticate with Twitter credentials:
    stream_auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    stream_auth.set_access_token(OAUTH_TOKEN, OATH_TOKEN_SECRET)

    # Authorize the Stream API
    # Create the api to connect to twitter with your creadentials
    stream_api = tweepy.API(stream_auth)

    wait_on_rate_limit= True;  # will make the api to automatically wait for rate limits to replenish
    wait_on_rate_limit_notify= True;  # will make the api  to print a notification when Tweepyis waiting for rate limits to replenish\

    # Stream Listener && Collect to MongoDB
    class StreamListener(tweepy.StreamListener):
        counter = 0
        
        def __init__(self, max_tweets=1000, *args, **kwargs):
            self.max_tweets = max_tweets
            self.counter = 0
            super().__init__(*args, **kwargs)
            
        def on_connect(self):
            self.counter = 0

        def on_status(self, status):
            
            # make sure the collected tweets are unique
            abc = tweet_collection.find_one({'id_str': status.id})
            if abc!=None:
                print("same data in collection")
                return 
            
            ### Store tweet to MongoDB      
            # get some text
            #print(self.counter)
            #print(status.text)
            
            # After Get Full text
            # Check if Retweet
            if hasattr(status, "retweeted_status"):  
                try:
                    print(status.retweeted_status.extended_tweet["full_text"])
                    full_text1 = status.retweeted_status.extended_tweet["full_text"]
                    StreamListener.collectToMongo(self,self.counter,status.id,full_text1)
                except AttributeError:
                    print(status.retweeted_status.text)
                    full_text2 = status.retweeted_status.text
                    StreamListener.collectToMongo(self,self.counter,status.id,full_text2)
            else:
                try:
                    print(status.extended_tweet["full_text"])
                    full_text3 = status.extended_tweet["full_text"]
                    StreamListener.collectToMongo(self,self.counter,status.id,full_text3)
                except AttributeError:
                    print(status.text)
                    full_text4 = status.text
                    StreamListener.collectToMongo(self,self.counter,status.id,full_text4)
                    
            # count max tweet
            if self.counter >= self.max_tweets:
                stream.disconnect()  
                
        def on_error(self, status_code):
            if status_code == 420:
                return False
            
        def collectToMongo(self,counter,idTweet,full_text):
            # collection stucture
            new_tweet = {
                'id_doc': counter,
                'id_str': idTweet,
                'full_text': full_text,
            }
            tweet_collection.insert_one(new_tweet)
            
            # Increment counter
            self.counter += 1
            print("============== ",self.counter, "documents insert ==============\n\n")

        
    # Connect to a streaming API
    # number of returned tweets
    max_tweets = 10    
    # define the keywords, tweets contain election                                
    # keywords = ["#ThreeManDown",
    #     "อนุทิน"
    #    ]
    # defin the location, in Harrisonburg, VA
    # geocode = "38.4392897,-78.9412224,50mi" 
    stream_listener = StreamListener(max_tweets)
    stream = tweepy.Stream(auth=stream_api.auth, listener=stream_listener)
    stream.filter(track=keywords)

    # Pull data form tweet_collection to variable tweet_json
    tweet_json = list(tweet_collection.find())

    # collect all word that cut uaeless word
    all_tweet = ""
    for i in range(tweet_collection.count_documents({})):
        all_tweet += cutword(tweet_json[i]['full_text'])+"\n"

    # drop collection
    tweet_collection.drop()
    
    return all_tweet
        
###############################################################

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

#############################################################

def wordcloudThai(all_tweet):

    #แบ่งคำ
    words = word_tokenize(all_tweet)
    print(words)

    #ใช้ช่องว่างในการแยกคำ
    all_words = ' '.join(words).lower().strip()

    # stop word  เอา word ออก
    stopwords = {'\n','.','\\',"\'",'/','#'} # set
    print(type(stopwords))
    print(stopwords)

    #สร้าง object ของ wordcloud
    wordcloud = WordCloud(
        # font_path 
        font_path='font_path/Fahkwang-Medium.ttf',
        #regular expression สระ 
        regexp=r"[ก-๙a-zA-Z']+",
        #use stop word
        stopwords=stopwords,
        #size picture
        width=2000, height=2000,
        #text horizontal(นอน) 90%,text vertical 10%
        prefer_horizontal=.9,
        #จำนวนคำที่มีความถี่มากที่สุดที่นำมาสร้าง wordcloud
        max_words=40, 
        #type of color
        colormap='tab20c',
        #bg color
        background_color = 'white').generate(all_words)
    #plot image
    plt.figure(figsize = (10, 9))
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.show()
