# ibscraper
An web scraper and test randomizer for IB Physics 1

Scrapes http://fcis.aisdhaka.org/ to download IB Physics exams, then reads them and takes questions to create randomized tests

Current features:

  Updating from website
  
  Writing Paper 1 questions to file
  
To do:
  Write 30 Paper 1 questions to a single HTML file
  
  Write Paper 2 and 3 questions to file
  
  Extract images from PDF documents
  
  HL Tests!
  
Dependencies:

  BeautifulSoup
  
  PDFMiner
  
  Python3
  
Note: I'm using the Python3 port of PDFMiner, as it does not natively support Python3. It can be found here: https://pypi.python.org/pypi/pdfminer3k
