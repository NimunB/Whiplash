# Whiplash
A data art piece that aims to subvert our expectations of news headlines, and the counties they originate from.
Presented at the University of Waterloo's end of term FINE/CS 383 Exhibition.
Video: https://youtu.be/ZacUwuQO5II
Article: https://uwaterloo.ca/computer-science/news/art-computing

## Artist Statement
This is a data art piece that displays alternating positive and negative news headlines about various counties in the U.S. A Google Street View image of a random location in that county is also displayed. The concept behind the artwork relates to bringing balance to the way we interact with news, including multiple truths in our relationship with the news, and subverting our expectations of “good” and “bad” areas. This piece showcases news and images from the top and bottom ~500 counties in the U.S. based on poverty percentage. Counties with the lowest poverty are shown with negative headlines, and counties with the highest poverty are shown with positive headlines. 

## Technical Description
I used separate python scripts for image and news headline retrieval. To present the data in the visual way that I intended, I used p5.js. 

### Code Structure and Flow
The original SAIPE poverty data by county came from the 2022 SAIPE State and Country Estimates for 2022. I loaded this into Google Sheets.

I set up a Google Service account so that I could access this google sheet and my google drive from my python script image_retrieval.py. This script uses the Google Street View API to search for the county name and try to find an image for it. If an image is found, it is appropriately named, loaded into a Google Drive folder called 'CS 383/A3/images', and its name is listed in the “Image Found” column of the “Image Gathering” sheet in this Google spreadsheet. If an image is not found, that column is populated with “No”.

For all the top and bottom 500 counties for which we found an image, I put into a new worksheet under the same parent Google sheet called “Headline Gathering”. Depending on if it was a top or bottom county, I populated the “Headline Type” column with either “Bad” or “Good”. For headline gathering, I used many different APIs, and used a slightly different python script for each one. They are all stored in the news_retrieval folder. I primarily used SERP API and the news_retrieval_SERPAPI.py script because it was not throttling me at all while the others were. These python scripts also used the Google Service account I created to access and edit the Google sheet, and to use Google’s Natural Language Processing API. For each record, the python script checks if it is meant to find a good or bad headline. Depending on the type, it will add either a positive or negative random word out of a selection to the search query string. It will feed this search query into the news api and get the top 5 results. It will feed each of these 5 results into the Natural Language Processing API and pick the best headline and populate the “Headline” column of the spreadsheet. If no suitable headline was found (sentiment scores were not positive or negative enough), “N/A” is written instead in that column.

I then split the “Headline Gathering” data into two worksheets: “Good Place, Bad Headline”, and “Bad Place, Good Headline” depending on the headline type we had for that county. I downloaded both sheets as .tsv files and saved them locally. I also downloaded the images folder.

My sketch.js file calls the getRandomSlide() method every 17 seconds. This method selects a random record from one of the tables depending on what the last headline shown was. Each record contains the county name, state, image name, and headline. Using the image name, the right image is chosen from the local images folder. It alternates positive and negative headlines. Fill and stroke colors for the headline are shown depending on the type it is (‘Good’ or ‘Bad’). 

### Key Aspect
All of the counties from the SAIPE_Data included “County” in the name. In my first pass of using the Google Street View API to find images, I found that I only found images for around 800 out of the more than 3000 county records. I noticed that when I removed “County” from the county name, the API was more successful. So I processed this data in multiple passes, tweaking the query string each time, since sometimes Google does not refer to that county with “County” in the name.

I also noticed that recent positive headlines were really hard to come across for some counties, and I decided to add a positive word (e.g. charity, community, hero) to the search string, as well as set a minimum sentiment score in order to ensure I was getting actual positive results for the county.

