import requests
from bs4 import BeautifulSoup
import re
from tabulate import tabulate
from pymongo import MongoClient
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')
nltk.download('stopwords')

def scrape_bbc_news(url): 
  response=requests.get(url)
  if response.status_code==200:
     soup=BeautifulSoup(response.content,'html.parser')
     
     hotnews_headlines =[]
     hotnews_descriptions=[]
     hotnews_word_counts=[]
     hot_news = soup.find_all('div',class_="sc-adfaf101-3 hHYUcg")
     
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

  #if not text.strip():
      #return None

  text = text.lower()

  text = re.sub(r'http\S+','',text)
  text = re.sub(r'[^a-zA-Z\s]','',text)
  #text = re.sub(r'\s+','',text).strip()

  tokens=word_tokenize(text)
  
  tokens=[word for word in tokens if word.isalpha()]

  stop_words=set(stopwords.words('english'))
  filtered_tokens=[word for word in tokens if word not in stop_words]

  return ' '.join(filtered_tokens)

  return text


url="https://www.bbc.com/business"
hotnews_headlines, hotnews_descriptions, hotnews_word_counts=scrape_bbc_news(url)

print("HotNews")
hotnews_data=[["Headline","Description","Wordcount"]]
if hotnews_headlines and hotnews_descriptions and hotnews_word_counts:
  for headline, description, word_count in zip(hotnews_headlines, hotnews_descriptions,hotnews_word_counts):
      hotnews_data.append([headline, description, word_count])
#print(tabulate(hotnews_data, headers="firstrow"))


def mongodb_connection():
  client = MongoClient('mongodb://localhost:27017/')
  db = client['bbc_news_collection']
  connection= ['hotnews_collection']
  return connection
def insert_Data(data):
  table = mongodb_connection()
  table.insert_many(data)
def create_and_populate_db():
  url="https://www.bbc.com/business"
  news_Table= scrape_bbc_news(url)
  print(hotnews_data,"************")
  insert_Data(news_Table)
create_and_populate_db()
#if__name__=="__main__":
 