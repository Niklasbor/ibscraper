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
import random

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
    print("Done.")
    print("Writing files. This may take a minute...")
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
    print("OK. Sorting tests...")
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
    
    print("Done.")
    
    try:
        os.mkdir("Tests")
    except:
        pass
            
    os.chdir("Tests")    
    
    count = 0
    question = []
    new_question = False
    print ("Reading paper 1s...")
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
        print("Read " + fname)
    testlist = []
    print("Done.")
    print("Writing 30 random paper 1 questions...")
    for n in range(0, 30):
        testlist.append(paper1questions[random.randint(0, len(paper1questions) - 1)])
            
    with open("test.txt", 'w') as f:
        for n, x in enumerate(testlist):
            for y in x:
                f.write(y)
            print("Wrote question number " + str(n+1))
            
    print("Reading paper 2s...")
    for fname in paper2s:
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
                if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                    text = lt_obj.get_text()
                    if len(question) == 0:
                        question.append(text)
                    if ('A1.' in text or 'A2.' in text) or ('A1.' in text or 'A3.' in text) or ('A2.' in text or 'A3.' in text):
                        paper2questions.append(question)
                        question = [text]
                    else:
                        question.append(text)
    testlist2 = []
    print("Done.")
    print("Writing 3 random paper 2 questions...")
    for x in range (0, 3):
        testlist2.append(paper2questions[random.randint(0, len(paper2questions) - 1)])
    with open('test.txt', 'a') as f:
        for n, y in enumerate(testlist2):
            for z in y:
                f.write(z)
            print("Wrote question number " + str(n+1))
    print("Your new test is saved as test.txt. Be sure to move it out of this directory or the next time you do this errors will be thrown.")

def run():
    instring = input("Welcome to Niklas's IB Physics web scraper and test randomizer! What would you like to do? (u for update, r for randomize) ")
    if instring == 'u':
        get()
    if instring == 'r':
        randomize()
        
run()