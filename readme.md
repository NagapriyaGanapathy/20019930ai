# CA 2 PROGRAMMING
# WEB SCRAPING PROJECT
**Module Title:**  Programming for Data Analysis
**Module Code:** B9AI108
**Module leader:** Paul Laird
**Student Name:** Nagapriya Ganapathy
**Student ID:** 20019930

## BBC NEWS - DATA PIPELINE
# Project Overview :
The main goal of the project appears to be to gather news data from the BBC Business section,process the text to remove noise ,and store the cleaned data in a MongoDB database for futher analysis.

# KEY FEATURES :
# Step 1: Web Scraping
* !pip install pymongo is used to install the "pymongo" package,facilitating intraction with MongoDB databases within the python environment.
* BeautifulSoup parses HTML and XML documents,requests library for making HTTP requests in python.
* Scraped the data including Business news headline,description & news tags from the BBC news website.
  
# Step 2: Data Preprocessing:
Here, the scraped data were cleaned before storing into the Database,
* .strip() remove leading and trailing whitespace characters from
* .lower() converts strings into lowercase for consistency in Queries & avoid duplicate entries
* regular expression [^a-zA-Z\s] matches any character that is not a letter or whitespace.
* regular expression [http\S+] matches any substring that start with "http"

  # step 3: MongoDB Storage:
  * The preprocessed data is saved in a MongoDB database called "bbcnews"
  * The news data information is stored in a database connection "hotnews_collection"
  * Function mongodb_connection() makes connection to MongoDB instance
  * insert_Data() inserting the data into MongoDB collection



