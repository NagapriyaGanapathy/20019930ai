import requests
from bs4 import BeautifulSoup
import re
from tabulate import tabulate
from pymongo import MongoClient

def scrape_bbc_news(url):
  response=requests.get(url)
  if response.status_code==200:
     soup=BeautifulSoup(response.content,'html.parser')
     #print(soup)
     hotnews_headlines =[]
     hotnews_descriptions=[]
     hotnews_word_counts=[]
     hot_news = soup.find_all('div',class_="sc-adfaf101-3 hHYUcg")
     #print(hot_news)
     for news in hot_news:
         
         headline = news.find('h2', {'data-testid':'card-headline'}).text.strip()
         description = news.find('p',{'data-testid':'card-description'}).text.strip()

         headline = preprocess_text(headline)
         description=preprocess_text(description)

         if headline is not None and description is not None:
           hotnews_headlines.append(headline)
           hotnews_descriptions.append(description)

           word_count = len(description.split())
           hotnews_word_counts.append(word_count)
     return hotnews_headlines,hotnews_descriptions, hotnews_word_counts

  else:
      print("Failed to fetch page:",response.status_code)
      return None, None, None

##Preprocessing the data
def preprocess_text(text):
  if text is None:
      return None

  if not text.strip():
      return None

  #text = text.lower()

  text = re.sub(r'http\S+','',text)
  text = re.sub(r'[^a-zA-Z\s]','',text)
  #text = re.sub(r'\s+','',text).strip()

  return text


url="https://www.bbc.com/business"
hotnews_headlines, hotnews_descriptions, hotnews_word_counts=scrape_bbc_news(url)

print("HotNews")
hotnews_data=[["Headline","Description","Wordcount"]]
if hotnews_headlines and hotnews_descriptions and hotnews_word_counts:
  for headline, description, word_count in zip(hotnews_headlines, hotnews_descriptions,hotnews_word_counts):
      hotnews_data.append([headline, description, word_count])
print(tabulate(hotnews_data, headers="firstrow"))


def mongodb_connection():
  client = MongoClient('mongodb://localhost:27017/')
  db = client['bbc_news_collection']
  connection= ['hotnews_collection']
  return connection
def insert_Data(data):
  table = mongodb_connection()
  table.insert_many(data)
def fetch_Data(data):
  table_data=mongodb_connection()
  final_Data = list(table_data.find({},{'_id':0}))
  return final_Data
def create_and_populate_db():
  url=""
  news_Table= scrape_bbc_news(url)
  insert_Data=(news_Table)
