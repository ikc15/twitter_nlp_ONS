from textblob import TextBlob
import pandas as pd
import textpreprocessing as tp
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import ast 
import numpy as np
import os
import nltk 
import seaborn as sns
import matplotlib.pyplot as plt

hashtag = "brexit50p"

headers_for_basic_files = ["created_at", "id", "text", "entities", "source", 
                           "user.id", "user.screen_name", "user.location", 
                           "user.followers_count", "user.friends_count", 
                           "user.verified", "user.statuses_count", "geo", "coordinates",
                           "place_name", "user_location2", "retweet_count", 
                           "tweet_favorite_count", "tweet_favorited", "tweet_retweeted"]

class sentiment_analyser:
    def __init__(self, file_name, tweet_column_name):
        self.file_name = file_name
        self.tweet_column_name = tweet_column_name

        self.df = pd.read_csv(filepath_or_buffer = self.file_name, sep = ",", 
                              error_bad_lines=False)
        self.df.columns = headers_for_basic_files
        self.tweet_col = self.df[self.tweet_column_name]    
        
    def textblob_sentiment(self, text):
        return TextBlob(text).sentiment.subjectivity

    def nltk_sentiment(self, text):
        sid = SentimentIntensityAnalyzer()
        return sid.polarity_scores(text)["compound"]
    
   # def flair_sentiment(self, text):
        # this issue is that they've just trained their pre-trained model on the IMDB dataset!!!
     #   classifier = TextClassifier.load("en-sentiment")
      #  sentence = Sentence(text)
       # classifier.predict(sentence)
        #sentiment_polarity = ast.literal_eval(str(sentence.labels[0]).split(" ")[1])
        #return sentiment_polarity
        
    def aggregate_sentiment_analysis(self):
        
        sentiment_scores = []
        
        for i,tweet in enumerate(self.tweet_col.values):
            preprocessed_tweet = tp.clean_doc(tweet)
            mean_sentiment = np.mean([self.textblob_sentiment(preprocessed_tweet), 
                                      self.nltk_sentiment(preprocessed_tweet)])
                                      #self.flair_sentiment(preprocessed_tweet)])
            sentiment_scores.append(mean_sentiment)
        
        self.df["Sentiment Polarity"] = sentiment_scores
        
final_dict = {}
directory = "/Users/johannesheyl/Dropbox/PhD/Group_Project/twitter_nlp_ONS/ScrapingTwitterRealTime/datasets/"

dates = ["28/01/2020", "29/01/2020", "30/01/2020", "31/01/2020", "01/02/2020",
         "02/02/2020", "03/02/2020",]
folders = ["scrape_data_2020-01-28-2020-01-29", "scrape_data_2020-01-29-2020-01-30", 
           "scrape_data_2020-01-30-2020-01-31", "scrape_data_2020-01-31-2020-02-01", 
           "scrape_data_2020-02-01-2020-02-02", "scrape_data_2020-02-02-2020-02-03",
           "scrape_data_2020-02-03-2020-02-04"]

for i,date in enumerate(dates):
   print(i)
   corresponding_folder = folders[i]
   sa = sentiment_analyser(directory + corresponding_folder + "/" + hashtag + ".csv", "text")
   sa.aggregate_sentiment_analysis()
   final_dict[date] = sa.df["Sentiment Polarity"].to_numpy()
   
list_of_df = []

for i, date in enumerate(dates):
    list_of_df.append(pd.DataFrame.from_dict({date: final_dict[date]}))

i = pd.concat(list_of_df, ignore_index=True, axis=1)

df = i.melt(var_name='date', value_name='Average sentiment')
ax = sns.violinplot(x="date", y="Average sentiment", data=df)
plt.title("Sentiment Analysis of Tweets containing #" + hashtag) 
          
fig = ax.get_figure()

fig.savefig(hashtag)

"""
for file in os.listdir(directory):
    sa = sentiment_analyser(directory, "text")
    sa.aggregate_sentiment_analysis()
"""    


