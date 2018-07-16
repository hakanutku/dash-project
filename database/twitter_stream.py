import json
import sqlite3
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from sentiment_model.use_model import predict

with open('../passwords.txt', 'r') as file:
    passwords = {}
    for line in file.readlines():
        variable, value = (w.strip() for w in line.split('='))
        passwords[variable.lower()] = value

ACCESS_TOKEN = passwords['access_token']
ACCESS_TOKEN_SECRET = passwords['access_token_secret']
CONSUMER_KEY = passwords['consumer_key']
CONSUMER_SECRET = passwords['consumer_secret']

conn = sqlite3.connect("twitter.db")
c = conn.cursor()

search_query = "lcwaikiki"

class listener(StreamListener):

    def on_data(self, data):
        try:
            data = json.loads(data)
            id = data["id"]
            username = data["user"]["screen_name"]
            location = data["user"]["location"]
            date = data["created_at"]
            keyword = search_query
            text = data["text"]
            if "RT @" in text:
                return True
            sentiment = predict([text])[0]
            favoriteCount = data["favorite_count"]
            retweetCount = data["retweet_count"]
            imageurl = data["user"]["profile_image_url"]

            print(username, text)

            c.execute("""INSERT INTO twitter(id, username, location, date, keyword, text, sentiment,
                favoriteCount, retweetCount, imageurl) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (id, username, location, date, keyword, text, sentiment, favoriteCount, retweetCount, imageurl))
            conn.commit()
        except KeyError as e:
            print(str(e))
        return True

    def on_error(self, status):
        print(status)

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

twitterStream = Stream(auth, listener())
print("Starting Stream.")
twitterStream.filter(track=[search_query])
