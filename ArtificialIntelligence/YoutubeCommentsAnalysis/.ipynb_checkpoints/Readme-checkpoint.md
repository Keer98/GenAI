<h2>Project Overview</h2>

This Python project analyzes sentiment in YouTube comments for a specified video. It performs the following tasks:

Fetches Comments: Retrieves comments from the target video using the youtube_comment_downloader library.
Saves Comments: Stores the comments in a CSV file with columns for author, comment text, and time.
Preprocesses Text: Cleans and prepares the comment text for sentiment analysis by:
Lowercasing text
Removing punctuation
Tokenizing words
Removing stop words
Analyzes Sentiment: Calculates sentiment scores using the VADER (Valence Aware Dictionary and sEntiment Reasoner) lexicon from the nltk library. Scores include:
compound: Overall sentiment score (positive, negative, or neutral)
Categorizes Comments: Classifies comments as positive, negative, or neutral based on their compound scores.
Generates Reports:
Prints statistics on the sentiment distribution (positive, negative, neutral)
Creates a pie chart visualizing the comment sentiment distribution
Calculates the mean compound score for all comments
Groups comments by hours ago and calculates the mean compound score for each group
Visualizes the mean sentiment score over time