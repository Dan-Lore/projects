import requests
import re
from bs4 import BeautifulSoup


url = 'https://shikimori.me/animes/51458'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


result = requests.get(url, headers=headers)
soup = BeautifulSoup(result.text, "html.parser")

with open('test.html', 'w', encoding='utf-8') as html:
    html.writelines(soup.prettify())

with open('answer.txt', 'w', encoding='utf-8') as answer:
    desc = soup.body.find('div', attrs={'class':'b-text_with_paragraphs'}).text
    desc = re.sub(r'(?<=[.!?])(?=[^\s])', r'\n', desc)
    #print(desc)

    score_value = soup.body.find('div', attrs={'class':'score-value'}).text
    score_notice = soup.body.find('div', attrs={'class': 'score-notice'}).text
    #print(score_value, score_notice)

    