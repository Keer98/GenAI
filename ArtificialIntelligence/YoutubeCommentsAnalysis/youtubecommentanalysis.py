from youtube_comment_downloader import YoutubeCommentDownloader
import pandas as pd
import csv
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import matplotlib.pyplot as plt
import numpy as np
import schedule

'''downloader = YoutubeCommentDownloader()

# YouTube video URL or video ID
video_id = "kivUsDGWojU"  # or use the full URL: 'https://www.youtube.com/watch?v=LFWrc10Kb1w'

# Open a CSV file to save comments
with open("youtube_comments.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Author", "Comment", "Time"])  # Header with time included

    # Fetch and write comments
    for comment in downloader.get_comments(video_id):
        writer.writerow([comment["author"], comment["text"], comment["time"]])'''

df = pd.read_csv("youtube_comments.csv")
print(df.head())

def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Tokenize the text
    tokens = word_tokenize(text)
    # Remove stop words
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    return filtered_tokens

def analyze_sentiment(text):
    tokens = preprocess_text(text)
    sentiment = sia.polarity_scores(' '.join(tokens))
    
   
    return sentiment

# Create a SentimentIntensityAnalyzer object
sia = SentimentIntensityAnalyzer()
# Apply the sentiment analysis function to each review
df['sentiment'] = df['Comment'].apply(analyze_sentiment)
print(df)

df['compound'] = df['sentiment'].apply(lambda x: x['compound'])
print(df['compound'])

positive_comments = df[df['compound'] > 0.5]
negative_comments = df[df['compound'] < -0.5]
neutral_comments = df[(df['compound'] >= -0.5) & (df['compound'] <= 0.5)]
perc_neg_comments=len(negative_comments )/len(df)
perc_neg_comments
if perc_neg_comments< 0.3:
    print("Good Song")
elif perc_neg_comments> 0.6:
    print("Bad Song")
else:
    print("Song is not Good/Bad")

# Calculate the number of reviews in each category
positive_count = len(positive_comments)
negative_count = len(negative_comments)
neutral_count = len(neutral_comments)

    # Create a list of labels and corresponding counts
labels = ['Positive Comments', 'Negative Comments', 'Neutral Comments']
sizes = [positive_count, negative_count, neutral_count]

    # Create the pie chart
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()

def convert_to_hours_ago(time_str):
    if "hour" in time_str:
        return int(time_str.split(" ")[0])
    elif "day" in time_str:
        return int(time_str.split(" ")[0]) * 24
    elif "minute" in time_str:
        return 0  # assuming minutes ago is recent, so we use 0 hours
    return np.nan

df['hours_ago'] = df['Time'].apply(convert_to_hours_ago)
print(df.head())

print(df['compound'].mean())

# Group by 'hours_ago' and calculate the mean compound score
grouped_df = df.groupby('hours_ago')['compound'].mean().reset_index()

# Print the grouped DataFrame
print(grouped_df)
plt.plot(grouped_df['hours_ago'], grouped_df['compound'])
plt.xlabel('Hours Ago')
plt.ylabel('Mean Compound Score')
plt.title('Mean Sentiment Over Time')
plt.grid(True)
plt.show()