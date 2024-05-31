from GoogleNews import GoogleNews
from google.cloud import language_v2
from google.oauth2.service_account import Credentials
import gspread
from datetime import datetime
import random
import time

# Define a list of bad words
bad_words = ["awful", "disastrous", "gun", "drugs", "kill", "crash", "fire", "corrupt", "murder", "injure", "suicide", "gang", "shooting", "kidnap", "rape", "brutality", "harass", "burglary"]
good_words = ["success", "charity", "win", "happy", "exciting", "hardworking", "brilliant", "feat", "reward", "good", "praise", "celebrate", "pride", "joy", "goodwill", "helpful", "reuinte", "good samaritan", "feeding", "hope", "startup", "funding", "art", "creativity"]

# Dictionary mapping state abbreviations to full state names
state_abbreviations = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California",
    "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia",
    "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa",
    "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri",
    "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey",
    "NM": "New Mexico", "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio",
    "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont",
    "VA": "Virginia", "WA": "Washington", "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming"
}

# News and Sentiment API credentials
news_credentials = Credentials.from_service_account_file('./_private/credentials.json')

# Define the scope of the credentials and authenticate with Google Sheets
sheets_scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
sheets_credentials = Credentials.from_service_account_file('./_private/credentials.json', scopes=sheets_scope)
client = gspread.authorize(sheets_credentials)

#Initialize Google News and Google Sheets Client
googlenews = GoogleNews(start='01/01/2023', end='31/03/2024', lang='en')
sheetsClient = gspread.authorize(sheets_credentials)

# Open the Google Sheets file
sheet = sheetsClient.open('SAIPE_Data')

# Access the "Headline Gathering" sheet
worksheet = sheet.worksheet('Headline Gathering')

# Fetch records from the sheet starting from row 3
records = worksheet.get('A3:Z')

# Loop through each record
for index, record in enumerate(records[:1729]):
    if len(record) == 8 and index > 1672: # Want to find a headline for this record
        headline_type = record[7]
        state_abbreviation = record[2]
        state_name = state_abbreviations.get(state_abbreviation, state_abbreviation)  # Get full state name or keep abbreviation if not found
        headline_query = f"{record[3]} {state_name}" #E.g. Weston County WY
        if headline_type == "Bad":
           random_bad_word = random.choice(bad_words)
           headline_query = f"{headline_query} {random_bad_word}"
        if headline_type == "Good":
           random_good_word = random.choice(good_words)
           headline_query = f"{headline_query} {random_good_word}"
        print(headline_query)
        
        # Fetch news for query
        googlenews.search(headline_query)

        # Fetch news from the first 5 pages
        googlenews.get_page(1)

        # Get the combined result from all pages
        result = googlenews.result()

        # Initialize Google Sentiment Analysis API client
        client = language_v2.LanguageServiceClient(credentials=news_credentials)

        # Initialize variables to store the best title/media/datetime and its sentiment score
        min_score = 0
        max_score = 0
        best_title = 'N/A'
        best_media = ''
        best_datetime = ''
        best_score = ''

        # Iterate through each news title and perform sentiment analysis - First 5 headlines only
        for news_item in result[:5]:
            
            title = news_item['title']
            media = news_item['media']
            datetime = str(news_item['datetime'])

            # Take this out when you want to manuakky pick the top headline - do result[:1]
            """
            best_title = title
            best_media = media
            best_datetime = datetime
            """
            
            # Perform sentiment analysis on the news title
            document = {"content": title, "type_": language_v2.Document.Type.PLAIN_TEXT, "language_code": "en"}
            sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
              
            # Get sentiment score
            score = sentiment.score
            magnitude = sentiment.magnitude

            # Update most positive title if current score is higher
            if score > max_score and headline_type == "Good":
              best_title = title
              best_media = media
              best_datetime = datetime
              max_score = score
              best_score = max_score
            elif score < min_score and headline_type == "Bad":
              best_title = title
              best_media = media
              best_datetime = datetime
              min_score = score
              best_score = min_score
            
        
        # Clear result list before doing next place's search
        googlenews.clear()

        # Write headline details on google sheets
        worksheet.update_cell(index + 3, 9, best_title)  # Update Headline column
        worksheet.update_cell(index + 3, 10, best_score)  # Update Sentiment Rating column
        worksheet.update_cell(index + 3, 11, best_media)  # Update Publisher column
        worksheet.update_cell(index + 3, 12, best_datetime)  # Update Date column

        # Sleep for 3 seconds to not overload
        time.sleep(3)
        

