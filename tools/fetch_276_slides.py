#!/usr/bin/env python2.6
import os
import sys
import logging
import urllib2
import sgmllib
from os.path import basename
from urlparse import urlsplit


urlString='http://www.stanford.edu/class/cs276/cs276-2012-syllabus.html'

class MyParser(sgmllib.SGMLParser):
    "A simple parser class."

    def parse(self, s):
        "Parse the given string 's'."
        self.feed(s)
        self.close()

    def __init__(self, verbose=0):
        "Initialise an object, passing 'verbose' to the superclass."

        sgmllib.SGMLParser.__init__(self, verbose)
        self.hyperlinks = []

    def start_a(self, attributes):
        "Process a hyperlink and its 'attributes'."

        for name, value in attributes:
            if name == "href":
                self.hyperlinks.append(value)

    def get_hyperlinks(self):
        "Return the list of hyperlinks."

        return self.hyperlinks


def url2name(url):
    return basename(urlsplit(url)[2])

def download(url, localFileDir = None):
    localName = url2name(url)
    req = urllib2.Request(url)
    r = urllib2.urlopen(req)
    if r.info().has_key('Content-Disposition'):
        # If the response has Content-Disposition, we take file name from it
        localName = r.info()['Content-Disposition'].split('filename=')[1]
        if localName[0] == '"' or localName[0] == "'":
          localName = localName[1:-1]
    elif r.url != url: 
        # if we were redirected, the real file name we take from the final URL
        localName = url2name(r.url)
    if localFileDir: 
        # we can force to save the file as specified name
        localName = localFileDir + localName
    f = open(localName, 'wb')
    f.write(r.read())
    f.close()
    
def get_url_content(urlString):
	urlContent = urllib2.urlopen(urlString)
	s = urlContent.read()
	myparser = MyParser()
	myparser.parse(s)
	wfh = open('/Users/xyz/tmp/cs276/hypelinks.txt','w')
	print myparser.get_hyperlinks()
	for link in  myparser.get_hyperlinks():
		
		if 'handouts' in link and 'pdf' in link:
			 if  'http' in link:
			 	 pass
			 else:
			 	 file_link = 'http://www.stanford.edu/class/cs276/'+link
			 	 print file_link
			 	 localFileDir = '/Users/xyz/tmp/cs276/'
			 	 download(file_link, localFileDir)
	
	wfh.close()
	


def main():
    get_url_content(urlString)

if __name__ == '__main__':
  sys.exit(main())