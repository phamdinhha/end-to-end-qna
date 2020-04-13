import nltk
nltk.download('punkt')
from nltk import sent_tokenize
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import requests
from googlesearch import search

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

def customsearch(question, numberOfAnswer = 10):
    links = []
    for i in search(question, num=numberOfAnswer, stop=numberOfAnswer, pause=2):
        links.append(i)
        return links


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def documentGenerator(url):
    req = Request(url, headers=headers) 
    html = urlopen(req).read()
    soup = BeautifulSoup(html, 'lxml')
    for invisible_elem in soup.find_all(['script', 'style']):
        invisible_elem.extract()

    paragraphs = [p.get_text() for p in soup.find_all("p")]
    for para in soup.find_all('p'):
        para.extract()

    for href in soup.find_all(['a','strong']): 
        href.unwrap()
    text = soup.get_text(separator='\n\n')
    text = re.sub('\n +\n','\n\n',text)

    paragraphs += text.split('\n\n')
    paragraphs = [re.sub(' +',' ',p.strip()) for p in paragraphs]
    paragraphs = [p for p in paragraphs if len(p.split()) > 10]

    for i in range(0,len(paragraphs)):
        sents = []
        text_chunks = list(chunks(paragraphs[i],100000))
        for chunk in text_chunks:
            sents += sent_tokenize(chunk)
        sents = [s for s in sents if len(s) > 2]
        sents = ' '.join(sents)
        paragraphs[i] = sents
    
    paragraph = '\n\n'.join(paragraphs)
    regex_list = re.findall(r"\[(.*?)\]", paragraph)
    for regex in regex_list:
      paragraph = paragraph.replace("["+regex+"]", " ")
    regex_list = re.findall(r"\((.*?)\)", paragraph)
    for regex in regex_list:
      paragraph = paragraph.replace("("+regex+")", " ")
      paragraph = paragraph.replace("  ", "")

    return paragraph


