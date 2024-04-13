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
     #hot_news = soup.find_all('div',class_="sc-22e6e77d-2 jEcfdb")
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
  table = mongodb_connection()
  table.insert_many(data)
def fetch_datetime():
  url=""
  response =requests.post(url)
  if response.status_code ==200:
    data=response.json
    return data.get("datetime")

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
  if news_data:
    insert_Data(news_data)
    print("Data inserted into MongoDB successfully")
  else:
    print("No data inserted")
  
create_and_populate_db()
#if__name__=="__main__":

app = Flask(__name__)
@app.route('/datetime',methods=['post'])
def get_datetime():
  now=datetime.now()
  current_time=now.strftime("%Y-%m-%d %H:%M:%S")
  return jsonify({"datetime":current_time})

  if __name__ == '__main__':
    app.run(debug=True)

                 
