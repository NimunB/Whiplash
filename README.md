# Whiplash
A data art piece that aims to subvert our expectations of news headlines, and the places they originate from. Powered by Google's Sentiment Analysis, Streetview API, and News.

Presented at the University of Waterloo's end of term FINE/CS 383 Exhibition.

Video: https://youtu.be/ZacUwuQO5II

Article: https://uwaterloo.ca/computer-science/news/art-computing

<img width="566" alt="Screen Shot 2024-05-31 at 1 03 36 AM" src="https://github.com/NimunB/Whiplash/assets/32827637/8f23222c-27e6-4621-949e-b03be78c8af7">

_Showing negative headline for top 500 county_

<img width="531" alt="Screen Shot 2024-05-31 at 1 03 02 AM" src="https://github.com/NimunB/Whiplash/assets/32827637/9bf7c05b-59bf-4346-8a30-e1ba941919f3">

_Showing positive headline for bottom 500 County_


## Artist Statement
This is a data art piece that displays alternating positive and negative news headlines about various counties in the U.S. A Google Street View image of a random location in that county is also displayed. The concept behind the artwork relates to bringing balance to the way we interact with news, including multiple truths in our relationship with the news, and subverting our expectations of “good” and “bad” areas. This piece showcases news and images from the top and bottom ~500 counties in the U.S. based on poverty percentage. Counties with the lowest poverty are shown with negative headlines, and counties with the highest poverty are shown with positive headlines. 

### Formal Qualities

A huge component of this artwork is the data that is driving it. The process behind getting the data was divided into three components: 

- A: Getting poverty estimates by county
- B: Finding images for each county
- C: Retrieving a positive or negative headline for the county

Part A involved accessing the 2022 SAIPE State and Country Estimates for 2022, which organized all the U.S. counties by their poverty percentage.

Part B involved feeding the county name into the Google Street View API to get an image for that county.

Part C involved feeding the county name and a randomly generated positive or negative word into a news API (GoogleNews, SerpAPI, etc.), and then feeding the top 5 headlines returned from that search into the Google Natural Language API to get the sentiment scores, and saving the most positive or negative headline.

For the top 500 counties, I saved negative headlines to show, and for the bottom 500 counties, I saved positive headlines to show. The result was having the image and headline information saved for the counties I wanted to display in Google spreadsheets.

### Context
This artwork is about our news and how we consume it. 

#### Balance
The news that we see on both large-scale and local media outlets is overwhelmingly negative. It can create a really bleak view of the world around you. I wanted to create an experience which temporarily allowed for a more balanced way to consume the news. I wanted viewers to see positive news just as much as they saw negative news. This is why I chose to alternate them back and forth. This might be jarring to certain users, and might be a form of visual whiplash. It is intended to jolt you a little. In my opinion, mixed surprise that conveys the range of the human experience is better than solely negative surprise that only fills you with dread. Also, that alternation between positive and negative news forces you to mindfully pay attention to each, rather than mindlessly and hopelessly consuming it.

#### Multiple Truths
When we see negative news about an incident, we oftentimes do not get to see what the place it happened in looked like. That place is only defined by a very negative incident that happened there. That however is only one truth. By including a normal, suburban looking image of the place in its natural state, viewers might understand that a headline is not enough to define a place. Multiple truths must be considered.

Also, that event and the place it occurred in can seem distant to us. By including a relatable and suburban image of the place, we might connect to it a bit more. We might spend half a second more feeling rather than numbly consuming.

#### Subverting our Expectations of Good and Bad Areas
Since positive headlines are shown for “poorer” counties and negative headlines are shown for “richer” counties, it might make certain viewers who are familiar with those counties question their beliefs and expectations. What makes an area “good” or “bad”? How much of that has to do with how we consume media coming out of a certain area?

#### Ken Lum
After the project was complete, I looked up the artist Ken Lum and found that his photography-based works like Portrait-Repeated Text Series and Death and Furniture have a really similar style to mine - a long form image (in his case portraits)  with a shorter graphic and colorful text. Both our work is about intersections. His are between race, gender, work, and stress, and mine are between news, poverty, community, and mood. 


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

