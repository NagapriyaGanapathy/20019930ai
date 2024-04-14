import requests
from bs4 import BeautifulSoup
import re
from tabulate import tabulate
from pymongo import MongoClient
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from spellchecker import SpellChecker
from datetime import datetime
import pytz
import nltk
nltk.download('punkt')
nltk.download('stopwords')

## Scraping data from BBC news website using scrape_bbc_news() method.
def scrape_bbc_news(url):
  response=requests.get(url)
  if response.status_code==200:
     soup=BeautifulSoup(response.content,'html.parser')

     hotnews_headlines =[]
     hotnews_descriptions=[]
     hotnews_description_counts=[]
     hotnews_tag=[]

     hot_news = soup.find_all('div',class_="sc-adfaf101-3 hHYUcg")
     current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

     for news in hot_news:

         headline = news.find('h2', {'data-testid':'card-headline'}).text.strip()
         description = news.find('p',{'data-testid':'card-description'}).text.strip()
         tag=news.find('span',{'data-testid':'card-metadata-tag'}).text.strip()

         headline = preprocess_text(headline)
         description=preprocess_text(description)
         tag=preprocess_text(tag)

         if headline is not None and description is not None and tag is not None:
           hotnews_headlines.append(headline)
           hotnews_descriptions.append(description)
           hotnews_tag.append(tag)

           word_count = len(description.split())
           hotnews_description_counts.append(word_count)

     date_time=[current_time]*len(hotnews_headlines)
     return hotnews_headlines,hotnews_descriptions, hotnews_description_counts,hotnews_tag,date_time

  else:
      print("Failed to fetch page:",response.status_code)
      return None, None, None,None,None

##Preprocessing the scraped data
def preprocess_text(text):
  if text is None:
      return None

  if not text.strip():
      return None

  text = text.lower()
  text = re.sub(r'http\S+','',text)
  text = re.sub(r'[^a-zA-Z\s]','',text)
  tokens=word_tokenize(text)
  tokens=[word for word in tokens if word.isalpha()]
  stop_words=set(stopwords.words('english'))
  tokens=[word for word in tokens if word not in stop_words]

  spell = SpellChecker()
  corrected_tokens=[]
  for word in tokens:
      corrected_word=spell.correction(word)
      if corrected_word is not None:
        corrected_tokens.append(corrected_word)

  return ' '.join(corrected_tokens)

  return text


url="https://www.bbc.com/business"
hotnews_headlines, hotnews_descriptions, hotnews_description_counts,hotnews_tag,date_time=scrape_bbc_news(url)


print("HotNews:")
hotnews_data=[["Headline","Description","Wordcount","tag","Date and Time"]]
if hotnews_headlines and hotnews_descriptions and hotnews_description_counts and hotnews_tag and date_time:
  for headline, description, word_count,tag,date_time in zip(hotnews_headlines, hotnews_descriptions,hotnews_description_counts,hotnews_tag,date_time):
      hotnews_data.append([headline, description, word_count,tag,date_time])
print(tabulate(hotnews_data, headers="firstrow"))


def mongodb_connection():
  client = MongoClient('mongodb://localhost:27017/')
  db = client['bbc_news_collection']
  connection= db['hotnews_collection']
  return connection
def insert_Data(data):
  try:
     table = mongodb_connection()
     table.insert_many(data)
     print("Data inserted")
  except Exception as e:
     print(e)

def create_and_populate_db():
  url="https://www.bbc.com/business"
  hotnews_headlines, hotnews_descriptions, hotnews_description_counts,hotnews_tag,date_time=scrape_bbc_news(url)

  news_data=[]
  for headline, description, word_count,tag,date_time in zip(hotnews_headlines, hotnews_descriptions,hotnews_description_counts,hotnews_tag,date_time):
    news_data.append({
        "headline":headline,
        "description":description,
        "word_count":word_count,
        "tag":tag,
        "date_time":date_time

    })
  existing_data=list(mongodb_connection().find({},{"headline":1,"_id":0}))
  unique_news_data=[]
  for data in news_data:
    if data["headline"]not in [existing["headline"]for existing in existing_data]:
      unique_news_data.append(data)
  
  if unique_news_data:
    insert_Data(unique_news_data)
    print("Unique Data inserted into MongoDB successfully")
  else:
    print("No unique data inserted")
  
create_and_populate_db()
#if__name__=="__main__":


                 
