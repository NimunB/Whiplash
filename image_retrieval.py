import gspread
from google.oauth2.service_account import Credentials
import google_streetview.api
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import json
from io import BytesIO
import requests
from PIL import Image
import os

# Define the scope of the credentials and authenticate with Google Sheets
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
credentials = Credentials.from_service_account_file('./_private/credentials.json', scopes=scope)
client = gspread.authorize(credentials)

# Define url for metadata request
metadata_url = "https://maps.googleapis.com/maps/api/streetview/metadata"

# Build the Google Drive service
drive_service = build('drive', 'v3', credentials=credentials)

# Open the Google Sheets file
sheet = client.open('SAIPE_Data')

# Access the "Image Gathering" sheet
worksheet = sheet.worksheet('Image Gathering')

# Fetch records from the sheet starting from row 5
records = worksheet.get('A5:Z')

# Folders to save images
gdrive_folder_id = '1gKfliyydtc48bGx0Lq9uhmaHta5wiM_H' # Path: 'CS 383/A3/images'
local_folder = 'images'

# Load API key from auth.json
with open('_private/auth.json') as auth_file:
    auth = json.load(auth_file)
    api_key = auth["API_KEY"]

# Loop through each record
for index, record in enumerate(records[:3199]):
    #if len(record) < 7: # Only do it if we haven't searched for it already
    if record[6] == "No": # Only do it if we haven't found an image yet
      name = record[3]
      name = name.split(" County")[0] # Remove County from name
      postal_code = record[2]
      
      # Combine name and postal code
      location = f"{name} {postal_code}, USA"

      # Name images like 0000, 0001, etc.
      filename = f"{index:04d}.jpg"

      # Define parameters for Google Street View API metadata request
      metadata_params = {
          'location': location,
          'key': api_key
      }
      
      # Request metadata for the location
      metadata_response = requests.get(metadata_url, params=metadata_params)
      metadata = metadata_response.json()

      # Save image if found, otherwise mark as 'No' in the sheet
      if metadata['status'] == 'OK':
          print(filename)
          # Define parameters for Google Street View API
          params = {
              'size': '1440x900',
              'location': location,
              'fov': 130,
              'key': api_key
          }
          
          # Make a request to Google Street View API
          response = requests.get("https://maps.googleapis.com/maps/api/streetview", params=params)
          """
          # Image found, save locally
          
          with open(os.path.join(local_folder, filename), 'wb') as f:
              f.write(response.content)
          """

          # Save to google drive folder: gdrive_folder
          file_metadata = {
              'name': filename,
              'parents': [gdrive_folder_id]  # specify the parent folder ID
          }
          media = MediaIoBaseUpload(BytesIO(response.content), mimetype='image/jpeg')
          drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
          
          # Update cell
          worksheet.update_cell(index + 5, 7, filename)  # Update "Image Found?" column
          
      else:
          # Image not found, update cell
          worksheet.update_cell(index + 5, 7, "No")  # Update "Image Found?" column
      