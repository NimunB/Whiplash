from GoogleNews import GoogleNews
from google.cloud import language_v2
from google.oauth2.service_account import Credentials

credentials = Credentials.from_service_account_file('./_private/credentials.json')

#Initialize Google News API
googlenews = GoogleNews(start='01/01/2023', end='31/03/2024', lang='en', region='US')

# Fetch news for a specific query
googlenews.search('Weston County WY')

# Fetch news from the first 5 pages
for i in range(1, 6):
    googlenews.get_page(i)

# Get the combined result from all pages
result = googlenews.result()

# Initialize Google Sentiment Analysis API client
client = language_v2.LanguageServiceClient(credentials=credentials)

# Initialize variables to store the most positive title/media/datetime and its sentiment score
most_positive_title = ''
most_positive_media = ''
most_positive_datetime = ''
max_score = -1.0

# Iterate through each news title and perform sentiment analysis
for news_item in result:
    title = news_item['title']
    media = news_item['media']
    datetime = news_item['datetime']
    
    # Perform sentiment analysis on the news title
    document = {"content": title, "type_": language_v2.Document.Type.PLAIN_TEXT}
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
    
    # Get sentiment score
    score = sentiment.score
    magnitude = sentiment.magnitude

    # Update most positive title if current score is higher
    if score > max_score:
        most_positive_title = title
        most_positive_media = media
        most_positive_datetime = datetime
        max_score = score

    print(title, score, magnitude)

# Print the most positive title and its media source and datetime
print("Most Positive Title:", most_positive_title)
print("Most Positive Media Source:", most_positive_media)
print("Most Positive Datetime:", most_positive_datetime)


