"""
Python script for searching twitter data and saving it to a database(Twitter.db) file.
"""

import sqlite3

import pandas as pd
from twython import Twython
from yandex_translate import YandexTranslate

from database.sentiment_model.use_model import predict

translator = YandexTranslate("")

ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""
CONSUMER_KEY = ""
CONSUMER_SECRET = ""

twitter = Twython(app_key=CONSUMER_KEY, app_secret=CONSUMER_SECRET, oauth_token=ACCESS_TOKEN, oauth_token_secret=ACCESS_TOKEN_SECRET)

conn = sqlite3.connect("Twitter.db")
# c = conn.cursor()
# c.execute("""SELECT TOP 1 id FROM Twitter ORDER BY id""")
# min_id = c.fetchone()

def twitter_search(q, num_of_tweets=1000):
    print("Searching for {}".format(q))

    results = twitter.cursor(twitter.search, q=q)
    count = 0

    tweets = {
        "id": [],
        "username": [],
        "location": [],
        "date": [],
        "text": [],
        "translation": [],
        "favoriteCount": [],
        "retweetCount": [],
        "imageurl": []
    }

    for result in results:
        # if result["id"] < min_id:
        #     break

        if q.lower() in result["user"]["screen_name"].lower():
            continue
        if "RT @" in result["text"]:
            continue

        print(count)
        tweets["username"].append(result["user"]["screen_name"])
        tweets["location"].append(result["user"]["location"])
        tweets["id"].append(result["id"])
        tweets["date"].append(result["created_at"])
        tweets["text"].append(result["text"])

        try:
            tweets["translation"].append(translator.translate(result["text"], "en-tr")["text"][0])
        except YandexTranslateException:
            pass

        tweets["favoriteCount"].append(result["favorite_count"])
        tweets["retweetCount"].append(result["retweet_count"])
        tweets["imageurl"].append(result["user"]["profile_image_url"])

        count += 1
        if count == num_of_tweets:
            break

    tweets = pd.DataFrame.from_dict(tweets)
    tweets["sentiment"] = predict(tweets.translation)
    tweets["keyword"] = q

    return tweets

queries = ["lcwaikiki"]
dfs = [twitter_search(q=query) for query in queries]
data = pd.concat(dfs)

data.to_sql("Twitter", conn, if_exists="append", index=False)
