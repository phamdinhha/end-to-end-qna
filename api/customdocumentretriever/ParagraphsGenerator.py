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

class ParagraphGenerator:
    def __init__(self, question):
        self.paragraphs = self.paragraphsGenerator(question)

    def ggSearch(self, question):
        links = []
        prevLink = ""
        for j in search(question, lang='en', country='en', num=1, stop=8, pause=2):
            curLink = re.findall(r"\//(.*?)\/", j)[0]
            if (curLink != prevLink):
                links.append(j)
                prevLink = curLink
        return links

    def chunks(self, l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]

    def paragraphSearch(self, url):
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
        paragraphs = [re.sub(' +',' ',p.strip()) for p in paragraphs[:5]]
        paragraphs = [p for p in paragraphs if len(p.split()) > 50]

        # for i in range(0,len(paragraphs)):
        #     sents = []
        #     text_chunks = list(self.chunks(paragraphs[i],10000))
        #     for chunk in text_chunks:
        #         sents += sent_tokenize(chunk)
        #     sents = [s for s in sents if len(s) > 2]
        #     sents = ' '.join(sents)
        #     paragraphs[i] = sents

        paragraph = '\n\n'.join(paragraphs)
        regex_list = re.findall(r"\[(.*?)\]", paragraph)
        for regex in regex_list:
            paragraph = paragraph.replace("["+regex+"]", " ")
        regex_list = re.findall(r"\((.*?)\)", paragraph)
        for regex in regex_list:
            paragraph = paragraph.replace("("+regex+")", " ")
        paragraph = paragraph.replace("  ", "")

        return paragraph

    def paragraphsGenerator(self, question):
        paras = []
        links = self.ggSearch(question)
        for link in links:
            para = self.paragraphSearch(link)
            if(para != ""):
                paras.append(para)
        return paras[0]