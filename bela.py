
import requests
from bs4 import BeautifulSoup
import re
import tweepy
from datetime import datetime
import tweepy
from keys import consumer_key, consumer_secret, access_key, access_token

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_key)
api = tweepy.API(auth)

source = requests.get('https://www.parlamento.pt/Paginas/UltimasIniciativasEntradas.aspx').text
soup = BeautifulSoup(source, 'lxml') 
my_divs = soup.find_all("div", {"class": "col-xs-10 margin_padding0"})
titles = []
memory_title = []
memory_text = []
for div in my_divs:
    clean_div = div.prettify()
    titles.append(clean_div)

for title in titles:
    soup2 = BeautifulSoup(title, 'lxml')
    tit = soup2.find('p', {'class': 'title'})
    desc = soup2.find('p', {'class': 'desc'})
    tweet = (" {} | publicado em {}. \n {}".format(tit.text, datetime, desc.text))
    if tit not in memory_title:
        title_content = [i for i in tit.text if i != '\n']
        title_content = ''.join(title_content)
        text_content = [i for i in desc.text if i != '\n']
        text_content = ''.join(text_content)
        content = [title_content, text_content]
        content = ''.join(content)
        if len(content) <= 280:
            api.update_status('{}|{}'.format(title_content, text_content))
        else:
            api.update_status('{}|{}'.format(title_content, text_content[270-len(title_content)]))
        memory_title.append(tit.text)
        memory_text.append(desc.text)
        break


if len(memory_title) >= 10:
    del memory_title [-1]


# ver pq n ta postando
# adicionar o link
# testar de novo aa postagem
# publicar no repositorio