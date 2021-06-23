from bs4 import BeautifulSoup
import re
from datetime import datetime
from keys import consumer_key, consumer_secret, access_key, access_token
import requests
import tweepy

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_key)
api = tweepy.API(auth)

source = requests.get('https://www.parlamento.pt/Paginas/UltimasIniciativasEntradas.aspx').text
soup = BeautifulSoup(source, 'lxml') 
my_divs = soup.find_all("div", {"class": "col-xs-10 margin_padding0"})
titles = []
content_memory = []
memory_title = []
memory_text = []

class getItem:
    def __getitem__(self,i):
        return f'Value {i}'

for div in my_divs:
    clean_div = div.prettify()
    titles.append(clean_div)

def update(content):
    first_update = [content[:270], '...']
    update = ''.join(first_update)  
    api.update_status(update)
        
def get_last_status():
    ids = []
    for status in api.user_timeline('isabellacmo'):
        ids.append(status.id)
    return ids[0]

def update_reply(link):
    api.update_status('@isabellacmo Para saber mais, acesse: {}{}'. format('https://www.parlamento.pt', link), in_reply_to_status_id = get_last_status())

import time


for title in titles:
    soup2 = BeautifulSoup(title, 'lxml')
    tit = soup2.find('p', {'class': 'title'})
    desc = soup2.find('p', {'class': 'desc'})
    link = soup2.find('a', href=True)
    if tit not in memory_title:
        title_content = [i for i in tit.text if i != '\n']
        title_content = ''.join(title_content)
        text_content = [i for i in desc.text if i != '\n']
        text_content = ''.join(text_content)
        content = [title_content, text_content]
        content = '\n'.join(content)
        memory_title.append(tit.text) # how to insert
        memory_text.append(desc.text)


        update(content)
        update_reply(link['href'])
        time.sleep(10)
        if len(content_memory) >= 10:
            del content_memory [-1]

