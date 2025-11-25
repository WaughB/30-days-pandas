import pandas as pd

data = [[1, 'Let us Code'], [2, 'More than fifteen chars are here!']]
tweets = pd.DataFrame(data, columns=['tweet_id', 'content']).astype({'tweet_id':'Int64', 'content':'object'})

def invalid_tweets(tweets: pd.DataFrame) -> pd.DataFrame:
    
    return tweets[tweets['content'].str.len() > 15][['tweet_id']]

print(invalid_tweets(tweets))