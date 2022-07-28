import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
from common import *

def SentimentAnalysis(polarity, subjectivity, title, color):
    plt.figure(figsize = (8,6))
    for i in range(0, polarity.shape[0]):
      plt.scatter(polarity, subjectivity, color = color)

    plt.title(title)
    plt.xlabel('Polarity')
    plt.ylabel('Subjectivity')
    plt.show()

def SentimentPercentages(df):
    counter_pos = 0
    counter_neg = 0
    counter_n = 0
    for i in range(0, len(df['SENTIMENT'])):
        if df['SENTIMENT'][i] == {'POSITIVE'}:
            counter_pos += 1
        elif df['SENTIMENT'][i] == {'NEGATIVE'}:
            counter_neg += 1
        else:
            counter_n += 1
    per_pos = counter_pos / len(df['SENTIMENT'])
    per_neg = counter_neg / len(df['SENTIMENT'])
    per_n = counter_n / len(df['SENTIMENT'])
    percentages = [per_pos, per_neg, per_n]
    return percentages


mydb = mysql.connector.connect(
    host      = "localhost"  ,
    user      = "root"       ,
    passwd    = ""           ,
    database  = db_name
)

if mydb.is_connected():
    print("Connected Successfully!")
    cur = mydb.cursor()

bmw_df = pd.read_sql(main_query(db_name, words[0]), con=mydb)
ferrari_df = pd.read_sql(main_query(db_name, words[1]), con=mydb)
mercedes_df = pd.read_sql(main_query(db_name, words[2]), con=mydb)

pol_bmw = pd.read_sql(pol_query(db_name, words[0]), con=mydb)
subj_bmw = pd.read_sql(subj_query(db_name, words[0]), con=mydb)

pol_ferrari = pd.read_sql(pol_query(db_name, words[1]), con=mydb)
subj_ferrari = pd.read_sql(subj_query(db_name, words[1]), con=mydb)

pol_mercedes = pd.read_sql(pol_query(db_name, words[2]), con=mydb)
subj_mercedes = pd.read_sql(subj_query(db_name, words[2]), con=mydb)

words_df = pd.read_sql(f'SELECT SRCH_WRD AS WORD FROM {db_name}.TWEETS', con=mydb)
words_list = []
for i in words_df.values:
    for j in i:
        words_list.append(j)




SentimentAnalysis(pol_bmw, subj_bmw, 'Sentiment Analysis for BMW', '#6fd02b')
SentimentAnalysis(pol_ferrari, subj_ferrari, 'Sentiment Analysis for Ferrari', '#2dd1d4')
SentimentAnalysis(pol_mercedes, subj_mercedes, 'Sentiment Analysis for Mercedes', '#2d74d4')



bmw_per = SentimentPercentages(bmw_df)
ferrari_per = SentimentPercentages(ferrari_df)
mercedes_per = SentimentPercentages(mercedes_df)

percentages_df = pd.DataFrame({
    'BMW':bmw_per,
    'FERRARI':ferrari_per,
    'MERCEDES':mercedes_per
},index = ['Positive', 'Negative', 'Neutral'])
percentages_df = percentages_df.transpose()

percentages_df.plot(kind='bar', colormap='Reds', grid=True, figsize=(13,5), title = "Percentages of Sentiment", xlabel = "Automobile Firms")