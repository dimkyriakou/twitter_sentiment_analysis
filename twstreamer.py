import re
import tweepy as tw
from textblob import TextBlob



def clean_tweet(txt):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\S+)", " ", txt).split())

def remove_emojis(txt):
    if txt:
        return txt.encode('ascii', 'ignore').decode('ascii')
    else:
        return None

def remove_urls(txt):
    return re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', txt)

class MyStreamListener(tw.StreamListener):
    def on_status(self, post):
        if post.retweeted:
            # Avoid retweeted info, and only original tweets will be received
            return True

        text = post.text
        # Pre-process the tweets
        text = remove_emojis(text) # Remove emojes from the text
        text = remove_urls(text) # Remove URLs from the text

        sentiment = TextBlob(text).sentiment
        polarity = sentiment.polarity
        subjectivity = sentiment.subjectivity

        if polarity > 0:
            sentiment = 'POSITIVE'
        elif polarity < 0:
            sentiment = 'NEGATIVE'
        else:
            sentiment = 'NEUTRAL'

        # The location from where the tweet was posted, based on coordinates
        longitude = None
        latitude = None
        if post.coordinates:
            longitude = post.coordinates['coordinates'][0]
            latitude = post.coordinates['coordinates'][1]

        # Collect the hashtags from a tweet
        hashtag_list = re.findall(r"#(\w+)", text)
        hashtags = ' '.join([str(hashtag) for hashtag in hashtag_list])
        print(post.text)

        # Add the search word of every tweet to a variable
        search_w_list= []
        for i in words:
            if i in text.upper():
                search_w_list.append(i)
                s_word = ' '.join([str(word) for word in search_w_list])


        if search_w_list != []:
            # Insert tweets in MySQL table "tweets"
            if mydb.is_connected():
                mycur = mydb.cursor()
                sql = "INSERT INTO {} (tweet_id, author, author_tweets, author_followers, created_at, text, num_retweets, longitude, latitude, hashtags, polarity, subjectivity, sentiment, search_word) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format("tweets")
                val = (post.id_str, post.user.screen_name, post.user.statuses_count, post.user.followers_count, post.created_at, clean_tweet(text), post.retweet_count, longitude, latitude, hashtags, polarity, subjectivity, sentiment, s_word)
                mycur.execute(sql, val)
                mydb.commit()
                mycur.close()

    def disconnect_steam(self, status_code):
        # Stop scraping when rate limit of api is reached
        if status_code == 420: # The error for reaching the rate limit is 420
            # return False to disconnect the stream
            return False