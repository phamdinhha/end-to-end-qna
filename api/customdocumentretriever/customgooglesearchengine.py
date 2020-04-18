import nltk
nltk.download('punkt')
from nltk import sent_tokenize
import re
from bs4 import BeautifulSoup
from bs4 import Comment
from urllib.request import urlopen, Request
import requests
from googlesearch import search
import csv
import datetime

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}


class CustomGoogleSearchEngine():
    def __init__(self, question, path_to_document_trunk = "./data/collecteddatafromgoogle.csv"):
        self.document_trunk = path_to_document_trunk
        self.question = question

    def buildDocumentTrunk(self):
        paragraphs = []
        links = self.customsearch(numberOfAnswer = 10)
        with open(self.document_trunk, 'w', encoding="utf8", newline='') as data_source:
            writer = csv.writer(data_source)
            writer.writerow(["date", "title", "link", "paragraphs"])
            for link in links:
                title, paragraphs = self.paragraphGenerator(link)
                writer.writerow([datetime.datetime.now(), title, link, paragraphs])
        print("Document trunk was built")
        return self.document_trunk


    def customsearch(self, numberOfAnswer = 10):
        links = []
        for i in search(self.question, num=numberOfAnswer, stop=numberOfAnswer, pause=1):
            links.append(i)
        return links


    def chunks(self, l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]

    def paragraphGenerator(self, url):
        req = Request(url, headers=headers) 
        html = urlopen(req).read()
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('title')
        for invisible_elem in soup.find_all(['script', 'style', 'head', 'title', 'meta', '[document]']):
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
            text_chunks = list(self.chunks(paragraphs[i],1000))
            for chunk in text_chunks:
                sents += sent_tokenize(chunk)
            sents = [s for s in sents if len(s) > 2]
            sents = ' '.join(sents)
            regex_list = re.findall(r"\[(.*?)\]", sents)
            for regex in regex_list:
                sents = sents.replace("["+regex+"]", " ")
            sents = sents.replace("  ", "")
            paragraphs[i] = sents

        if(len(paragraphs) > 10):
            return title, paragraphs[:10]
        return title, paragraphs



