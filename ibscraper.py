#!/usr/bin/env python

import urllib.request
import os
from bs4 import BeautifulSoup, SoupStrainer
import http.client
from io import StringIO, BytesIO
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTImage, LTFigure

def get():
    pagelist = []
    examlist = []
    print("Connecting to fcis.aisdhaka.org...")
    thing = http.client.HTTPConnection("fcis.aisdhaka.org")
    request = thing.request('GET', 'http://fcis.aisdhaka.org/personal/chendricks/IB/IB%20Site/practexams.html')
    response = thing.getresponse()
    print("Done. Crawling exam pages...")
    
    for link in BeautifulSoup(response, parse_only=SoupStrainer('a')):
        if link.has_attr('href'):
            pagelist.append(link['href'])
            
    for x in pagelist:
        if 'IB' in x:
            if ' ' in x:
                request2 = thing.request('GET', 'http://fcis.aisdhaka.org/personal/chendricks/IB/IB%20Site/IB%20' + x[3:6] + '%20Exams.htm')
                response2 = thing.getresponse()
                for link in BeautifulSoup(response2, parse_only=SoupStrainer('a')):
                    if link.has_attr('href'):
                        if 'SL' in link['href']:
                            examlist.append(link['href'])
                            print("Found http://fcis.aisdhaka.org/personal/chendriks/IB/IB%20Site/IB%20" + link['href'][3:6] + '%20Exams.htm')
            else:
                request2 = thing.request('GET', 'http://fcis.aisdhaka.org/personal/chendricks/IB/IB%20Site/' + x)
                response2 = thing.getresponse()
                for link in BeautifulSoup(response2, parse_only=SoupStrainer('a')):
                    if link.has_attr('href'):
                        if 'SL' in link['href']:
                            examlist.append(link['href'])
                            print("Found http://fcis.aisdhaka.org/personal/chendriks/IB/IB%20Site/" + link['href'])
    print("Done. Writing files. This may take a minute...")
    os.mkdir("Tests")
    os.chdir("Tests")
    
    for link in examlist:
        if '..' in link:
            if not "mark" in link:
                remotefile = urllib.request.urlopen('http://fcis.aisdhaka.org/personal/chendricks/IB/' + link[2:])
                localfile = open(link[33:], 'wb')
                localfile.write(remotefile.read())
                print("Wrote " + link[33:])
        else:
            if not "mark" in link:
                remotefile = urllib.request.urlopen('http://fcis.aisdhaka.org/personal/chendricks/IB/IB%20Site/' + link)
                localfile = open(link[10:], 'wb')
                localfile.write(remotefile.read())
                print("Wrote " + link[10:])
    print("Everything is up to date.")
    
def randomize():
    paper1s = []
    paper2s = []
    paper3s = []
    for (dirpath, dirnames, filenames) in os.walk("Tests"):
        for fname in filenames:
            if 'SL1' in fname and not 'a' in fname:
                paper1s.append(fname)
            if 'P1' in fname:
                paper1s.append(fname)
            if 'SL2' in fname and not 'a' in fname:
                paper2s.append(fname)
            if 'P2' in fname:
                paper2s.append(fname)
            if 'SL3' in fname and not 'a' in fname:
                paper3s.append(fname)
            if 'P3' in fname:
                paper3s.append(fname)
    
    paper1questions = []
    paper2questions = []
    paper3questions = []
    
    
    
    try:
        os.mkdir("Tests")
    except:
        pass
            
    os.chdir("Tests")    
    
    count = 0
    question = []
    new_question = False
    for fname in paper1s:
        infile = open(fname, 'rb')
        parser = PDFParser(infile)
        doc = PDFDocument()
        parser.set_document(doc)
        doc.set_parser(parser)
        doc.initialize('')
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for x, page in enumerate(doc.get_pages()):
            if x == 0:
                continue
            interpreter.process_page(page)
            layout = device.get_result()
            for n, lt_obj in enumerate(layout):
                if len(question) == 0:
                    question.append(lt_obj.get_text())
                elif isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                    text = lt_obj.get_text()
                    items = text.split()
                    try:
                        text2 = items[0]
                        OK1 = text2[1] == '.' or text2[2] == '.'
                        OK2 = text2[0].isdigit()
                        
                        new_question = OK1 and OK2
                        if new_question:
                            paper1questions.append(question)
                            question = [lt_obj.get_text()]
                        else:
                            question.append(lt_obj.get_text())
                    except:
                        continue
                elif isinstance(lt_obj, LTFigure):
                    print(lt_obj)
        for n, x in enumerate(paper1questions):
            for y in x:
                y.replace('\t', ' ')
                y.replace('\n', '')
            with open('test' + str(n) + '.txt', 'w') as f:
                if n>30:
                    for z in x:
                        f.write(z)    

def run():
    instring = input("Welcome to Niklas's IB Physics web scraper and test randomizer! What would you like to do? (u for update, r for randomize) ")
    if instring == 'u':
        get()
    if instring == 'r':
        randomize()
        
run()