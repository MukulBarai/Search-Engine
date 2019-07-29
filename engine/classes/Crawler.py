# Importing packages
import requests  
from . import urlParser
from . import dbHandler
from threading import Thread 
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# Coverting relative links into absolute links
def relToAbs(url, href):
    try:
        parsedUrl = urlparse(url)
        scheme = parsedUrl.scheme
        host = parsedUrl.hostname
        path = parsedUrl.path
        if(href[0:2] == "//"):
            return scheme + ":" + href
        elif(href[0] == "/"):
            return scheme + "://" + host + path + href
        elif(not(href[0:4] == "http")):
            return False
        else:
            return href
    except Exception as e:
        print("Exception in relToAbs function")
        return False

class storeUrls(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        try:
            mainUrl = dbHandler.getUrl()
            mainParser = urlParser.Parse(mainUrl)
            urls = mainParser.getUrls()
            self.store(mainUrl, urls)
        except Exception as e:
            print(e)
            return

    def store(self, mainUrl, urls):
        for url in urls:
            if(url == ""):
                continue
            if(url == "#"):
                continue
            absUrl = relToAbs(mainUrl, url)
            if(absUrl == False):
                continue
            try:
                parser = urlParser.Parse(absUrl)
                title = parser.getTitle()
                description = parser.getDescription()
                keywords = parser.getKeywords()
            except Exception as e:
                print(e)
                continue
            if(title == ""):
                continue
            if(not(dbHandler.ifUrlExists(absUrl))):
                try:
                    dbHandler.insertUrl(title, absUrl, description, keywords)
                    print("url inserted: " + absUrl)
                except Exception as e:
                    print(e)

class storeImgSrcs(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        try:
            mainUrl = dbHandler.getUrl()
            mainParser = urlParser.Parse(mainUrl)
            imgLinks = mainParser.getImgSrcs()
            self.store(mainUrl, imgLinks)
        except Exception as e:
            print(e)
            return

    def store(self, mainUrl, imgLinks):
        for imgLink in imgLinks:
            if(imgLink.has_attr('src')):
                src = imgLink['src']
            else:
                continue
            if(imgLink.has_attr('title')): 
                title = imgLink['title']
            else:
                title = ""
            if(imgLink.has_attr('alt')):
                alt = imgLink['alt']
            else:
                alt = ""
            absImgSrc = relToAbs(mainUrl, src)
            if(absImgSrc == False):
                continue

        if(not(dbHandler.ifImgSrcExists(mainUrl, absImgSrc))):
            try:
                dbHandler.insertSrc(mainUrl, absImgSrc, title, alt)
                print("image inserted: " + absImgSrc)
            except Exception as e:
                print(e)
def Crawl():
    storeUrls().start()
    storeImgSrcs().start()
